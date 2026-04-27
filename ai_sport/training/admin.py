from django.contrib import admin
from .models import UserProfile, TrainingPlan, TrainingExercise, TrainingSession, Achievement, UserAchievement


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'anonymous_mode', 'level', 'xp', 'streak_days', 'preferred_coach_type']
    list_filter = ['anonymous_mode', 'low_social_mode', 'preferred_coach_type']


@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_minutes', 'mood_tag', 'space_tag', 'silent_mode', 'xp_reward', 'is_active']
    list_filter = ['mood_tag', 'space_tag', 'is_active']


@admin.register(TrainingExercise)
class TrainingExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan', 'duration_seconds', 'order']
    list_filter = ['plan']


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'xp_earned', 'started_at', 'completed_at']
    list_filter = ['status', 'started_at']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'condition_type', 'condition_value', 'xp_reward', 'is_hidden']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'unlocked_at']
