# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ai/', views.ai, name='ai'),
    path('cybersecurity/', views.cybersecurity, name='cybersecurity'),
    path('gaming/', views.gaming, name='gaming'),
    path('trending/', views.trending, name='trending'),
]