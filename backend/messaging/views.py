from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Conversation, Message

@login_required
def users(request):
    # Only show users that are not the logged-in user
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')
    return render(request, "messaging/users.html", {"users": users})

@login_required
def view_user(request, user_id):
    viewed_user = get_object_or_404(User, id=user_id)
    return render(request, "messaging/view_user.html", {"viewed_user": viewed_user})

@login_required
def inbox(request):
    # Get all conversations for the logged-in user
    conversations = Conversation.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated_at')
    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required
def conversation(request, conversation_id):
    # Get the conversation or return a 404 error
    conversation = get_object_or_404(Conversation.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)), id=conversation_id)
    # Get all messages for the conversation
    messages = Message.objects.filter(conversation=conversation).order_by('created_at')
    return render(request, 'messaging/conversation.html', {'conversation': conversation, 'messages': messages})