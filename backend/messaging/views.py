from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Conversation, Message

@login_required
def users(request):
    """
    View to display a list of all users except the logged-in user.
    """
    # Only show users that are not the logged-in user
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')
    return render(request, "messaging/users.html", {"users": users})

@login_required
def view_user(request, user_id):
    """
    View to display details of a specific user.
    """
    viewed_user = get_object_or_404(User, id=user_id)
    return render(request, "messaging/view_user.html", {"viewed_user": viewed_user})

@login_required
def inbox(request):
    """
    View to display the inbox of the logged-in user, showing all conversations.
    """
    # Get all conversations for the logged-in user
    conversations = Conversation.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated_at')
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')
    return render(request, 'messaging/inbox.html', {'conversations': conversations, 'users': users})

@login_required
def new_chat(request):
    """
    View to start a new chat with another user. If a conversation already exists, redirect to that conversation.
    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        other_user = get_object_or_404(User.objects.exclude(id=request.user.id), id=user_id)

        # Check if a conversation already exists between the two users
        conversation = Conversation.objects.filter(
            (Q(user_one=request.user) & Q(user_two=other_user)) |
            (Q(user_one=other_user) & Q(user_two=request.user))
        ).first()

        # Otherwise, create a new conversation
        if not conversation:
            conversation = Conversation.objects.create(user_one=request.user, user_two=other_user)

        return redirect('conversation', conversation_id=conversation.id)

    # Display a list of users to start a new chat with, excluding the logged-in user
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')
    return render(request, 'messaging/conversation.html', {'users': users})

@login_required
def conversation(request, conversation_id):
    """
    View to display a specific conversation and its messages.
    """
    # Get the conversation or return a 404 error
    conversation = get_object_or_404(Conversation.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)), id=conversation_id)

    if request.method == 'POST':
        message_content = request.POST.get('content', '').strip()

        if message_content:
            Message.objects.create(conversation=conversation, sender=request.user, content=message_content)
            conversation.save()
            return redirect('conversation', conversation_id=conversation.id)

    # Get all conversations for the logged-in user and exclude the logged-in user from the list of users
    conversations = Conversation.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated_at')
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')

    # Get all messages for the conversation
    chat_messages = Message.objects.filter(conversation=conversation).order_by('created_at')
    return render(request, 'messaging/conversation.html', {'conversation': conversation, 'chat_messages': chat_messages, 'conversations': conversations, 'users': users})

@login_required
def edit_message(request, conversation_id, message_id):
    """
    View to edit a specific message.
    """
    
    conversation = get_object_or_404(Conversation.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)), id=conversation_id)
    
    message = get_object_or_404(Message, id=message_id, conversation=conversation, sender=request.user)

    if request.method == 'POST':
        
        content = request.POST.get('content', '').strip()
        
        if not content:
            return redirect('conversation', conversation_id=conversation_id)
        
        if content == message.content:
            return redirect('conversation', conversation_id=conversation_id)

        if content:
            message.content = content
            message.is_edited = True
            message.edited_at = timezone.now()
            message.save()
            
            return redirect('conversation', conversation_id=conversation_id)

@login_required
def delete_message(request, conversation_id, message_id):
    """
    View to delete a specific message.
    """
    conversation = get_object_or_404(Conversation.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)), id=conversation_id)
    
    message = get_object_or_404(Message, id=message_id, conversation=conversation, sender=request.user)

    if request.method == 'POST':
        message.is_deleted = True
        message.save()
        
        return redirect('conversation', conversation_id=conversation_id)