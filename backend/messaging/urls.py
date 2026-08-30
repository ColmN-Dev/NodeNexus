from django.urls import path
from . import views

# messaging/urls.py

urlpatterns = [
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.view_user, name='view_user'),
    path('messages/', views.inbox, name='inbox'),
    path('messages/new/', views.new_chat, name='new_chat'),
    path('messages/<int:conversation_id>/', views.conversation, name='conversation'),
    path('messages/<int:conversation_id>/edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('messages/<int:conversation_id>/delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]