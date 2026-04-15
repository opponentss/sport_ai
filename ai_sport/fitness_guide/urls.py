"""
健身指南模块URL路由配置

路由结构：
- /fitness-guide/                         → 健身指南首页
- /fitness-guide/diet/                     → 饮食分类首页
- /fitness-guide/diet/<category>/          → 饮食建议列表
- /fitness-guide/diet/<category>/add/       → 添加饮食建议（管理员）
- /fitness-guide/diet/<category>/<id>/      → 饮食建议详情
- /fitness-guide/muscles/                  → 肌肉认识首页
- /fitness-guide/muscles/<group_id>/        → 肌肉群列表
- /fitness-guide/muscles/<group_id>/<id>/   → 肌肉部位详情
- /fitness-guide/muscles/add-group/        → 添加肌肉群（管理员）
- /fitness-guide/muscles/<group_id>/add/   → 添加肌肉部位（管理员）
- /fitness-guide/equipment/                 → 器材分类首页
- /fitness-guide/equipment/<cat>/           → 器材列表
"""

from django.urls import path
from . import views

urlpatterns = [
    # 健身指南首页
    path('', views.fitness_guide_home, name='fitness_guide_home'),

    # 饮食建议路由
    path('diet/', views.diet_home, name='diet_home'),
    path('diet/<str:category>/', views.diet_list, name='diet_list'),
    path('diet/<str:category>/add/', views.diet_create, name='diet_create'),
    path('diet/<str:category>/<int:diet_id>/', views.diet_detail, name='diet_detail'),
    path('diet/<str:category>/<int:diet_id>/edit/', views.diet_update, name='diet_update'),
    path('diet/<str:category>/<int:diet_id>/delete/', views.diet_delete, name='diet_delete'),

    # 肌肉认识路由
    path('muscles/', views.muscle_home, name='muscle_home'),
    path('muscles/add-group/', views.muscle_group_create, name='muscle_group_create'),
    path('muscles/<int:group_id>/', views.muscle_group_list, name='muscle_group_list'),
    path('muscles/<int:group_id>/add/', views.muscle_item_create, name='muscle_item_create'),
    path('muscles/<int:group_id>/<int:muscle_id>/', views.muscle_detail, name='muscle_detail'),
    path('muscles/<int:group_id>/<int:muscle_id>/edit/', views.muscle_item_update, name='muscle_item_update'),
    path('muscles/<int:group_id>/<int:muscle_id>/delete/', views.muscle_item_delete, name='muscle_item_delete'),

    # 器材认识路由
    path('equipment/', views.equipment_knowledge, name='equipment_knowledge'),
    path('equipment/<str:category>/', views.equipment_list, name='equipment_list'),
    path('equipment/<str:category>/add/', views.equipment_create, name='equipment_create'),
    path('equipment/<str:category>/<int:equipment_id>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<str:category>/<int:equipment_id>/edit/', views.equipment_update, name='equipment_update'),
    path('equipment/<str:category>/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
]