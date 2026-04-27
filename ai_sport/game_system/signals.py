from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from checkin.models import Checkin
from meals.models import Meal
from sleep.models import SleepRecord
from .models import UserGameProfile, Achievement, UserAchievement, DailyMission, UserDailyMission


def get_or_create_profile(user):
    profile, _ = UserGameProfile.objects.get_or_create(user=user)
    return profile


def check_achievements(user):
    profile = get_or_create_profile(user)
    unlocked_ids = set(UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True))
    all_achievements = Achievement.objects.all()
    newly_unlocked = []

    for achievement in all_achievements:
        if achievement.id in unlocked_ids:
            continue

        condition_met = False
        ct = achievement.condition_type
        cv = achievement.condition_value

        if ct == 'total_checkins':
            condition_met = profile.total_checkins >= cv
        elif ct == 'total_exercise_minutes':
            condition_met = profile.total_exercise_minutes >= cv
        elif ct == 'total_meals':
            condition_met = Meal.objects.filter(user=user).count() >= cv
        elif ct == 'total_sleeps':
            condition_met = SleepRecord.objects.filter(user=user).count() >= cv
        elif ct == 'level_reach':
            condition_met = profile.level >= cv
        elif ct == 'strength_reach':
            condition_met = profile.strength >= cv

        if condition_met:
            UserAchievement.objects.create(user=user, achievement=achievement)
            profile.add_xp(achievement.xp_reward, 'exercise')
            newly_unlocked.append(achievement)

    return newly_unlocked


def update_daily_missions(user):
    today = timezone.now().date()

    missions = DailyMission.objects.filter(is_active=True)
    for mission in missions:
        user_mission, created = UserDailyMission.objects.get_or_create(
            user=user, mission=mission, date=today,
            defaults={'progress': 0, 'completed': False}
        )

        if user_mission.completed:
            continue

        if mission.mission_type == 'checkin':
            count = Checkin.objects.filter(user=user, date=today).count()
            user_mission.progress = count
        elif mission.mission_type == 'duration':
            from django.db.models import Sum
            total = Checkin.objects.filter(user=user, date=today).aggregate(s=Sum('duration'))['s'] or 0
            user_mission.progress = total
        elif mission.mission_type == 'meal':
            count = Meal.objects.filter(user=user, date=today).count()
            user_mission.progress = count
        elif mission.mission_type == 'sleep':
            count = SleepRecord.objects.filter(user=user, date=today).count()
            user_mission.progress = count

        if user_mission.progress >= mission.target_value:
            user_mission.completed = True
            user_mission.completed_at = timezone.now()
            profile = get_or_create_profile(user)
            profile.add_xp(mission.xp_reward, 'exercise')

        user_mission.save()


@receiver(post_save, sender=Checkin)
def on_checkin_saved(sender, instance, created, **kwargs):
    if not created:
        return

    profile = get_or_create_profile(instance.user)
    profile.total_checkins += 1
    profile.total_exercise_minutes += instance.duration
    profile.save()

    xp_earned = 10 + instance.duration
    profile.add_xp(xp_earned, 'exercise')

    check_achievements(instance.user)
    update_daily_missions(instance.user)


@receiver(post_save, sender=Meal)
def on_meal_saved(sender, instance, created, **kwargs):
    if not created:
        return

    profile = get_or_create_profile(instance.user)
    xp_earned = 10
    if instance.image:
        xp_earned += 5
    if instance.calories:
        xp_earned += 5

    profile.add_xp(xp_earned, 'meal')
    check_achievements(instance.user)
    update_daily_missions(instance.user)


@receiver(post_save, sender=SleepRecord)
def on_sleep_saved(sender, instance, created, **kwargs):
    if not created:
        return

    profile = get_or_create_profile(instance.user)

    quality_xp = {'excellent': 20, 'good': 15, 'fair': 10, 'poor': 5}
    xp_earned = quality_xp.get(instance.quality, 10)

    if instance.duration and instance.duration >= 7:
        xp_earned += 10

    profile.add_xp(xp_earned, 'sleep')
    check_achievements(instance.user)
    update_daily_missions(instance.user)
