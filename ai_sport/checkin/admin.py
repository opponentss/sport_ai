from django.contrib import admin
from .models import Checkin, ExerciseType


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty', 'calories_per_minute', 'is_active')
    list_filter = ('category', 'difficulty', 'is_active')
    search_fields = ('name',)


@admin.register(Checkin)
class CheckinAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'duration', 'calories_burned', 'date', 'time')
    list_filter = ('date',)
    search_fields = ('user__username', 'activity')
