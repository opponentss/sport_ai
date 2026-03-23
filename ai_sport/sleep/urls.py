from django.urls import path
from . import views

urlpatterns = [
    path('', views.sleep_list, name='sleep_list'),
    path('create/', views.sleep_create, name='sleep_create'),
    path('update/<int:pk>/', views.sleep_update, name='sleep_update'),
    path('delete/<int:pk>/', views.sleep_delete, name='sleep_delete'),
]
