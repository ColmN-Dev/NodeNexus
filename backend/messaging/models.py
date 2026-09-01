from django.db import models
from django.contrib.auth.models import User

# Conversation model to represent a chat between two users
class Conversation(models.Model):
    user_one = models.ForeignKey(User, related_name='conversations_as_user_one', on_delete=models.CASCADE)
    user_two = models.ForeignKey(User, related_name='conversations_as_user_two', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_one_archived = models.BooleanField(default=False)
    user_two_archived = models.BooleanField(default=False)
    
    # String representation of the Conversation model
    def __str__(self):
        return f"{self.user_one.username} & {self.user_two.username}"
    
# Message model to represent individual messages within a conversation
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    # String representation of the Message model, ending with a preview of the content
    def __str__(self):
        return f"Message from {self.sender.username}: {self.content[:50]}"
