"""
健身指南模块Django Admin配置

功能：
- 管理器材的增删改查
- 管理饮食建议的增删改查
- 管理肌肉群和肌肉部位的增删改查
"""

from django.contrib import admin
from .models import Equipment, DietItem, MuscleGroup, MuscleItem


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """器材管理"""
    list_display = ['name', 'category', 'image', 'video_url', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['category', 'name']


@admin.register(DietItem)
class DietItemAdmin(admin.ModelAdmin):
    """饮食建议管理"""
    list_display = ['title', 'category', 'is_featured', 'image', 'video_url', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['category', '-created_at']


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    """肌肉群管理"""
    list_display = ['name', 'latin_name', 'category', 'icon', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']


@admin.register(MuscleItem)
class MuscleItemAdmin(admin.ModelAdmin):
    """肌肉部位管理"""
    list_display = ['name', 'muscle_group', 'latin_name', 'is_featured', 'image', 'video_url', 'created_at']
    list_filter = ['muscle_group', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'training_tips']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['muscle_group', 'name']