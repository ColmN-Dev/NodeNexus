from django.urls import path
from . import views

# messaging/urls.py

urlpatterns = [
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.view_user, name='view_user'),
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:conversation_id>/', views.conversation, name='conversation'),
]