# core/urls.py

from django.urls import path
from . import views
from news.views import home, search_results, auto_complete, article_detail

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_results, name='search_results'),
    path("auto-complete/", auto_complete, name="auto_complete"),
    path('article/', article_detail, name='article_detail'),
    path('ai/', views.ai, name='ai'),
    path('cybersecurity/', views.cybersecurity, name='cybersecurity'),
    path('gaming/', views.gaming, name='gaming'),
    path('trending/', views.trending, name='trending'),
]