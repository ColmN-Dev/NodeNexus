from datetime import timedelta
from django.utils import timezone

from django.test import TestCase
from django.contrib.auth.models import User

from messaging.models import Conversation, Message, Notification

import cloudinary

class MessagingTestCase(TestCase):
    def test_users_page(self):
        
        user = User.objects.create_user(username='testuser', password='testpassword')
        
        cloudinary.config(cloud_name="test-cloud")
        
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get('/users/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging/users.html')
        
    def test_users_page_excludes_current_user(self):
        
        user1 = User.objects.create_user(username='user1', password='password1')
        user2 = User.objects.create_user(username='user2', password='password2')
        
        self.client.login(username='user1', password='password1')
        
        response = self.client.get('/users/')
        
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(user1, response.context['users'])
        self.assertIn(user2, response.context['users'])
        
    def test_view_user(self):
        
        user = User.objects.create_user(username='testuser', password='testpassword123_')
        
        viewed_user = User.objects.create_user(username='vieweduser', password='viewedpassword123_')
        
        self.client.login(username='testuser', password='testpassword123_')
        
        response = self.client.get(f'/users/{viewed_user.id}/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging/view_user.html')
        self.assertEqual(response.context['viewed_user'], viewed_user)
        
    def test_view_user_not_found(self):
        
        user = User.objects.create_user(username='testuser', password='testpassword123_')
        
        self.client.login(username='testuser', password='testpassword123_')
        
        response = self.client.get('/users/9999/')
        
        self.assertEqual(response.status_code, 404)
        
    def test_notifications(self):
        
        user = User.objects.create_user(username='testuser', password='testpassword123_')
        
        other_user = User.objects.create_user(username='otheruser', password='password123_')
        
        conversation = Conversation.objects.create(user_one=user, user_two=other_user)
        
        message = Message.objects.create(conversation=conversation, sender=other_user, content='Hello')
        
        Notification.objects.create(user=user, message=message)
        
        self.client.login(username='testuser', password='testpassword123_')
        
        response = self.client.get('/messages/notifications/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['message'], 'New message from otheruser')
        self.assertEqual(response.json()[0]['url'], f'/messages/{conversation.id}/')
        
    def test_notifications_only_returns_unread(self):
        
        user = User.objects.create_user(username="testuser", password="Password123_")
        
        other_user = User.objects.create_user(username="otheruser", password="Password123_")
        
        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        unread_message = Message.objects.create(conversation=conversation, sender=other_user, content="Unread message")
        
        read_message = Message.objects.create(conversation=conversation, sender=other_user, content="Read message")

        Notification.objects.create(user=user, message=unread_message)
        
        Notification.objects.create(user=user, message=read_message, is_read=True)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.get("/messages/notifications/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["message"], "New message from otheruser")
        
    def test_viewed_notification(self):
        
        user = User.objects.create_user(username="testuser", password="Password123_")
        
        other_user = User.objects.create_user(username="otheruser", password="Password123_")
        
        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        message = Message.objects.create(conversation=conversation, sender=other_user, content="Hello")

        notification = Notification.objects.create(user=user, message=message)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/notifications/{notification.id}/viewed/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)

        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
        
    def test_viewed_notification_not_owner(self):
        
        user1 = User.objects.create_user(username="user1", password="Password123_")
        
        user2 = User.objects.create_user(username="user2", password="Password123_")
        
        conversation = Conversation.objects.create(user_one=user1, user_two=user2)

        message = Message.objects.create(conversation=conversation, sender=user2, content="Hello")

        notification = Notification.objects.create(user=user1, message=message)

        self.client.login(username="user2", password="Password123_")

        response = self.client.post(f"/messages/notifications/{notification.id}/viewed/")

        self.assertEqual(response.status_code, 404)
        
        notification.refresh_from_db()
        self.assertFalse(notification.is_read)
        
    def test_inbox(self):
        
        user = User.objects.create_user(username="testuser", password="Password123_")
        
        other_user = User.objects.create_user(username="otheruser", password="Password123_")
        
        conversation = Conversation.objects.create(user_one=user, user_two=other_user)
        
        cloudinary.config(cloud_name="test-cloud")

        self.client.login(username="testuser", password="Password123_")

        response = self.client.get("/messages/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messaging/inbox.html")
        self.assertIn(conversation, response.context["conversations"])
        
    def test_inbox_excludes_archived_conversation(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user, user_one_archived=True)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.get("/messages/")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(conversation, response.context["conversations"])
        
    def test_new_chat(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post("/messages/new/", {"user_id": other_user.id})

        self.assertEqual(response.status_code, 302)

        conversation = Conversation.objects.get(user_one=user, user_two=other_user)
        self.assertEqual(response.url, f"/messages/{conversation.id}/")
        
    def test_new_chat_existing_conversation(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post("/messages/new/", {"user_id": other_user.id})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/messages/{conversation.id}/")
        self.assertEqual(Conversation.objects.count(), 1)
        
    def test_new_chat_cannot_chat_with_self(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post("/messages/new/", {"user_id": user.id})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Conversation.objects.count(), 0)
        
    def test_archive_conversation(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/{conversation.id}/archive/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/messages/")

        conversation.refresh_from_db()
        self.assertTrue(conversation.user_one_archived)
        
    def test_unarchive_conversation(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user, user_one_archived=True)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/{conversation.id}/unarchive/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/messages/")

        conversation.refresh_from_db()
        self.assertFalse(conversation.user_one_archived)
        
    def test_conversation_marks_messages_and_notifications_read(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")
        
        cloudinary.config(cloud_name="test-cloud")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        message = Message.objects.create(conversation=conversation, sender=other_user, content="Hello")

        notification = Notification.objects.create(user=user, message=message)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.get(f"/messages/{conversation.id}/")

        self.assertEqual(response.status_code, 200)

        message.refresh_from_db()
        notification.refresh_from_db()

        self.assertTrue(message.is_read)
        self.assertTrue(notification.is_read)
        
    def test_send_message(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/{conversation.id}/", {"content": "Hello friend"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/messages/{conversation.id}/")
        self.assertTrue(Message.objects.filter(conversation=conversation, sender=user, content="Hello friend").exists())
        
    def test_send_empty_message(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/{conversation.id}/", {"content": "   "})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Message.objects.filter(conversation=conversation).exists())
        
    def test_edit_message(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        message = Message.objects.create(conversation=conversation, sender=user, content="Original message")

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/{conversation.id}/edit_message/{message.id}/", {"content": "Edited message"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/messages/{conversation.id}/")

        message.refresh_from_db()
        self.assertEqual(message.content, "Edited message")
        self.assertTrue(message.is_edited)
        
    def test_edit_message_after_15_minutes(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        message = Message.objects.create(conversation=conversation, sender=user, content="Original message")

        message.created_at = timezone.now() - timedelta(minutes=16)
        message.save()

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/{conversation.id}/edit_message/{message.id}/", {"content": "Edited message"})

        self.assertEqual(response.status_code, 302)

        message.refresh_from_db()
        self.assertEqual(message.content, "Original message")
        self.assertFalse(message.is_edited)
    
    def test_delete_message(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        message = Message.objects.create(conversation=conversation, sender=user, content="Test message")

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/{conversation.id}/delete_message/{message.id}/")

        self.assertEqual(response.status_code, 302)

        message.refresh_from_db()
        self.assertTrue(message.is_deleted)
    
    def test_delete_conversation(self):

        user = User.objects.create_user(username="testuser", password="Password123_")

        other_user = User.objects.create_user(username="otheruser", password="Password123_")

        conversation = Conversation.objects.create(user_one=user, user_two=other_user)

        self.client.login(username="testuser", password="Password123_")

        response = self.client.post(f"/messages/{conversation.id}/delete/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/messages/")
        self.assertFalse(Conversation.objects.filter(id=conversation.id).exists())