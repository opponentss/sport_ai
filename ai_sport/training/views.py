from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db import models as db_models
from .models import (
    UserProfile, TrainingPlan, TrainingExercise,
    TrainingSession, Achievement, UserAchievement
)
from .forms import RegisterForm, ProfileSettingsForm
from .seed import seed_training_plans, seed_achievements


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'training/register.html', {'form': form})


@login_required
def home(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    today = timezone.now().date()
    today_session = TrainingSession.objects.filter(
        user=request.user,
        started_at__date=today,
    ).first()

    plans = TrainingPlan.objects.filter(is_active=True)
    recent_sessions = TrainingSession.objects.filter(user=request.user)[:5]

    ctx = {
        'profile': profile,
        'today_session': today_session,
        'plans': plans,
        'recent_sessions': recent_sessions,
        'has_trained_today': today_session is not None,
        'xp_progress': profile.xp % 100,
        'xp_to_next': 100 - (profile.xp % 100),
    }
    return render(request, 'training/home.html', ctx)


@login_required
def training_session(request, plan_id=None):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    plan = get_object_or_404(TrainingPlan, id=plan_id) if plan_id else None
    exercises = plan.exercises.all() if plan else []

    if request.method == 'POST':
        status = request.POST.get('status', 'completed')
        exercises_done = int(request.POST.get('exercises_done', 0))
        total = int(request.POST.get('exercises_total', 0))

        xp_earned = plan.xp_reward if plan else 10
        if status == 'partial':
            xp_earned = int(xp_earned * 0.5)
        elif status == 'skipped':
            xp_earned = int(xp_earned * 0.2)

        session = TrainingSession.objects.create(
            user=request.user,
            plan=plan,
            status=status,
            xp_earned=xp_earned,
            exercises_completed=exercises_done,
            exercises_total=total,
            completed_at=timezone.now(),
        )

        leveled_up = profile.add_xp(xp_earned)

        today = timezone.now().date()
        if profile.last_training_date:
            yesterday = today - timezone.timedelta(days=1)
            if profile.last_training_date == yesterday:
                profile.streak_days += 1
            elif profile.last_training_date < yesterday:
                profile.streak_days = 1
        else:
            profile.streak_days = 1
        profile.last_training_date = today
        profile.save()

        new_achievements = check_achievements(request.user, plan, status, today)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok',
                'xp_earned': xp_earned,
                'total_xp': profile.xp,
                'level': profile.level,
                'leveled_up': leveled_up,
                'streak_days': profile.streak_days,
                'new_achievements': [
                    {'name': a.name, 'icon': a.icon, 'description': a.description}
                    for a in new_achievements
                ],
            })

        msg = f'训练完成！+{xp_earned} XP'
        if leveled_up:
            msg += f' 🎉 升级到 Lv.{profile.level}！'
        messages.success(request, msg)
        return redirect('home')

    ctx = {
        'plan': plan,
        'exercises': exercises,
        'profile': profile,
    }
    return render(request, 'training/session.html', ctx)


@login_required
def quick_action(request, action):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if action == 'dont_want':
        plan = TrainingPlan.objects.filter(name='今天不想动', is_active=True).first()
        if plan:
            return redirect('training_session', plan_id=plan.id)
        return redirect('home')

    elif action == 'recommend':
        today = timezone.now().date()
        today_session = TrainingSession.objects.filter(
            user=request.user, started_at__date=today
        ).first()
        if today_session:
            messages.info(request, '你今天已经运动过了，休息一下吧')
            return redirect('home')

        from datetime import datetime
        hour = timezone.now().hour
        if hour >= 22 or hour < 6:
            plan = TrainingPlan.objects.filter(mood_tag='night', is_active=True).first()
        elif hour < 10:
            plan = TrainingPlan.objects.filter(mood_tag='low_energy', is_active=True).first()
        else:
            plan = TrainingPlan.objects.filter(mood_tag='normal', is_active=True).order_by('?').first()

        if plan:
            return redirect('training_session', plan_id=plan.id)
        return redirect('home')

    return redirect('home')


@login_required
def achievements_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    all_achievements = Achievement.objects.all()
    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).values_list('achievement_id', flat=True)

    ctx = {
        'profile': profile,
        'achievements': all_achievements,
        'user_achievements': user_achievements,
    }
    return render(request, 'training/achievements.html', ctx)


@login_required
def settings_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '设置已保存')
            return redirect('settings')
    else:
        form = ProfileSettingsForm(instance=profile)

    ctx = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'training/settings.html', ctx)


@login_required
def toggle_theme(request):
    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.dark_mode = not profile.dark_mode
        profile.save()
        from django.http import JsonResponse
        return JsonResponse({'dark_mode': profile.dark_mode})
    return redirect('home')


def check_achievements(user, plan, status, today):
    user_achievement_ids = set(
        UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
    )
    new_achievements = []

    for achievement in Achievement.objects.all():
        if achievement.id in user_achievement_ids:
            continue

        unlocked = False
        ct = achievement.condition_type
        cv = achievement.condition_value

        if ct == 'first_session':
            count = TrainingSession.objects.filter(user=user).count()
            unlocked = count >= cv
        elif ct == 'total_sessions':
            count = TrainingSession.objects.filter(user=user).count()
            unlocked = count >= cv
        elif ct == 'streak_days':
            profile = user.profile
            unlocked = profile.streak_days >= cv
        elif ct == 'total_xp':
            profile = user.profile
            unlocked = profile.xp >= cv
        elif ct == 'night_owl':
            count = TrainingSession.objects.filter(
                user=user,
                started_at__hour__gte=22,
            ).count()
            unlocked = count >= cv
        elif ct == 'gentle_soul':
            count = TrainingSession.objects.filter(
                user=user,
                plan__mood_tag='anxious',
            ).count()
            unlocked = count >= cv

        if unlocked:
            ua = UserAchievement.objects.create(user=user, achievement=achievement)
            user.profile.add_xp(achievement.xp_reward)
            new_achievements.append(achievement)

    return new_achievements
