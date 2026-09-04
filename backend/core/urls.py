from django.urls import path
from . import views

# core/urls.py

urlpatterns = [
    
    path('', views.home, name='home'),
    
    path('ai/', views.ai, name='ai'),
    
    path('cybersecurity/', views.cybersecurity, name='cybersecurity'),
    
    path('gaming/', views.gaming, name='gaming'),
    
    path('trending/', views.trending, name='trending'),
    
]