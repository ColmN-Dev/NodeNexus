"""
URL configuration for nodenexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
#config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    path('', include('core.urls')),
    
    path('', include('news.urls')),
    
    path('', include('accounts.urls')),
    
    path('', include('messaging.urls')),
    
]

# Error handlers (custom views for 404 and 500 errors)

handler404 = 'core.views.error_404'

handler500 = 'core.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)