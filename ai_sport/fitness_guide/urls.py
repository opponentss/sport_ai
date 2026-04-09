from django.urls import path
from . import views

urlpatterns = [
    path('', views.fitness_guide_home, name='fitness_guide_home'),
    path('diet/', views.diet_advice, name='diet_advice'),
    path('muscles/', views.muscle_knowledge, name='muscle_knowledge'),
    path('equipment/', views.equipment_knowledge, name='equipment_knowledge'),
]