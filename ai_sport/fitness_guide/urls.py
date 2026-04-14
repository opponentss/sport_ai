from django.urls import path
from . import views

urlpatterns = [
    path('', views.fitness_guide_home, name='fitness_guide_home'),
    path('diet/', views.diet_advice, name='diet_advice'),
    path('muscles/', views.muscle_knowledge, name='muscle_knowledge'),
    path('equipment/', views.equipment_knowledge, name='equipment_knowledge'),
    path('equipment/<str:category>/', views.equipment_list, name='equipment_list'),
    path('equipment/<str:category>/add/', views.equipment_create, name='equipment_create'),
    path('equipment/<str:category>/<int:equipment_id>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<str:category>/<int:equipment_id>/edit/', views.equipment_update, name='equipment_update'),
    path('equipment/<str:category>/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
]