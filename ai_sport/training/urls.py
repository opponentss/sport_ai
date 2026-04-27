from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('train/', views.training_session, name='training_start'),
    path('train/<int:plan_id>/', views.training_session, name='training_session'),
    path('quick/<str:action>/', views.quick_action, name='quick_action'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('settings/', views.settings_view, name='settings'),
]
