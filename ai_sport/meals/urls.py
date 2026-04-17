"""
餐饮管理模块URL路由配置
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.meal_list, name='meal_list'),
    path('create/', views.meal_create, name='meal_create'),
    path('update/<int:pk>/', views.meal_update, name='meal_update'),
    path('delete/<int:pk>/', views.meal_delete, name='meal_delete'),
    path('analyze/', views.analyze_food, name='analyze_food'),
]