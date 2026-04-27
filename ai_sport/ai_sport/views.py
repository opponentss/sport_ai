from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from checkin.models import Checkin
from meals.models import Meal
from sleep.models import SleepRecord
from user_profile.models import UserProfile
from game_system.models import UserGameProfile, UserDailyMission, Achievement, UserAchievement


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserGameProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'欢迎加入，冒险者 {username}！🏠')
                return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar_file = request.FILES['avatar']
        if avatar_file.content_type.startswith('image/'):
            profile.avatar = avatar_file
            profile.save()
            messages.success(request, '头像更新成功！')
        else:
            messages.error(request, '请上传图片文件！')
        return redirect('user_profile')

    checkin_count = Checkin.objects.filter(user=user).count()
    meal_count = Meal.objects.filter(user=user).count()
    sleep_count = SleepRecord.objects.filter(user=user).count()

    recent_checkins = Checkin.objects.filter(user=user).select_related('exercise_type').order_by('-date', '-time')[:5]
    recent_meals = Meal.objects.filter(user=user).order_by('-date', '-time')[:5]
    recent_sleeps = SleepRecord.objects.filter(user=user).order_by('-date')[:5]

    game_profile = UserGameProfile.objects.filter(user=user).first()

    total_calories = sum(c.calories_burned for c in Checkin.objects.filter(user=user) if c.calories_burned)
    total_exercise_minutes = game_profile.total_exercise_minutes if game_profile else 0
    today = timezone.now().date()
    daily_missions = UserDailyMission.objects.filter(
        user=user, date=today
    ).select_related('mission').order_by('-completed', 'mission__order')
    unlocked_achievements = Achievement.objects.filter(
        userachievement__user=user
    ).order_by('-userachievement__unlocked_at')[:8]

    context = {
        'user': user,
        'profile': profile,
        'checkin_count': checkin_count,
        'meal_count': meal_count,
        'sleep_count': sleep_count,
        'recent_checkins': recent_checkins,
        'recent_meals': recent_meals,
        'recent_sleeps': recent_sleeps,
        'game_profile': game_profile,
        'total_calories': total_calories,
        'total_exercise_minutes': total_exercise_minutes,
        'daily_missions': daily_missions,
        'unlocked_achievements': unlocked_achievements,
    }
    return render(request, 'user_profile/profile.html', context)
