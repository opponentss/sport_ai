from django.contrib import admin
from .models import UserGameProfile, Achievement, UserAchievement, DailyMission, UserDailyMission


@admin.register(UserGameProfile)
class UserGameProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'strength', 'endurance', 'agility', 'willpower', 'total_checkins')
    search_fields = ('user__username',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'condition_type', 'condition_value', 'xp_reward', 'is_hidden', 'order')
    list_filter = ('category', 'is_hidden')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'unlocked_at')


@admin.register(DailyMission)
class DailyMissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'mission_type', 'target_value', 'xp_reward', 'is_active', 'order')
    list_filter = ('mission_type', 'is_active')


@admin.register(UserDailyMission)
class UserDailyMissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'mission', 'date', 'progress', 'completed')
    list_filter = ('completed', 'date')
