from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkin_list, name='checkin_list'),
    path('create/', views.checkin_create, name='checkin_create'),
    path('update/<int:pk>/', views.checkin_update, name='checkin_update'),
    path('delete/<int:pk>/', views.checkin_delete, name='checkin_delete'),
]
