from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from .models import (
    UserGameProfile, Achievement, UserAchievement,
    DailyMission, UserDailyMission
)


def get_game_context(user):
    profile, _ = UserGameProfile.objects.get_or_create(user=user)
    achievements_count = UserAchievement.objects.filter(user=user).count()
    today = timezone.now().date()

    daily_missions = UserDailyMission.objects.filter(
        user=user, date=today
    ).select_related('mission').order_by('-completed', 'mission__order')

    return {
        'game_profile': profile,
        'achievements_count': achievements_count,
        'daily_missions': daily_missions,
        'xp_remaining': profile.xp_remaining,
        'xp_progress': profile.xp_progress,
        'level_title': profile.level_title,
    }


@login_required
def achievements_view(request):
    user = request.user
    unlocked = set(UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True))
    all_achievements = Achievement.objects.all()

    categories = {}
    for ach in all_achievements:
        cat_name = ach.get_category_display()
        if cat_name not in categories:
            categories[cat_name] = []
        categories[cat_name].append({
            'achievement': ach,
            'unlocked': ach.id in unlocked,
            'unlocked_at': UserAchievement.objects.filter(
                user=user, achievement=ach
            ).first().unlocked_at if ach.id in unlocked else None,
        })

    ctx = get_game_context(user)
    ctx['categories'] = categories
    ctx['total_achievements'] = all_achievements.count()
    ctx['unlocked_count'] = len(unlocked)

    return render(request, 'game_system/achievements.html', ctx)


@login_required
def leaderboard_view(request):
    user = request.user

    top_players = UserGameProfile.objects.select_related('user').order_by('-xp')[:50]
    user_profile = UserGameProfile.objects.filter(user=user).first()
    user_rank = None
    if user_profile:
        user_rank = UserGameProfile.objects.filter(xp__gt=user_profile.xp).count() + 1

    ctx = get_game_context(user)
    ctx['top_players'] = top_players
    ctx['user_rank'] = user_rank

    return render(request, 'game_system/leaderboard.html', ctx)
