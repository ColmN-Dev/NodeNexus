# core/urls.py

from django.urls import path
from . import views
from news.views import home, search_results, auto_complete

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_results, name='search_results'),
    path("auto-complete/", auto_complete, name="auto_complete"),
    path('ai/', views.ai, name='ai'),
    path('cybersecurity/', views.cybersecurity, name='cybersecurity'),
    path('gaming/', views.gaming, name='gaming'),
    path('trending/', views.trending, name='trending'),
]