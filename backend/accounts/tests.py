from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User
import cloudinary
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail

class SignUpTestCase(TestCase):
    def test_signup(self):
        
        response = self.client.post('/signup/', {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "Testpassword123_",
            "password2": "Testpassword123_"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser", email="testuser@example.com").exists())

    def test_invalid_signup(self):
        
        response = self.client.post('/signup/', {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "Testpassword123_",
            "password2": "Testpassword321_"
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser").exists())
        
class LoginTestCase(TestCase):
    def test_login(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        response = self.client.post('/login/', {
            "username": "testuser",
            "password": "Testpassword123_"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/')
        
    def test_invalid_login(self):
        response = self.client.post('/login/', {
            "username": "nonexistentuser",
            "password": "wrongpassword"
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password. Please correct the details below.")
        
class LogoutTestCase(TestCase):
    def test_logout(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        response = self.client.post('/logout/')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
class ProfileTestCase(TestCase):
    def test_profile_page(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        cloudinary.config(cloud_name="test-cloud")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        response = self.client.get('/profile/')
        
        self.assertEqual(response.status_code, 200)
        
    def test_username_change(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        response = self.client.post('/profile/', {
            "username": "newusername"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/')
        self.assertTrue(User.objects.filter(username="newusername").exists())
        
    def test_duplicate_username_change(self):
        
        User.objects.create_user(username="testuser1", email="testuser1@example.com", password="Testpassword123_")
        User.objects.create_user(username="testuser2", email="testuser2@example.com", password="Testpassword123_")
        
        self.client.login(username="testuser2", password="Testpassword123_")
        
        response = self.client.post('/profile/', {
            "username": "testuser1"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser2").exists())
        
    def test_preset_profile_picture(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        cloudinary.config(cloud_name="test-cloud")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        response = self.client.post('/profile/', {
            "preset_image": "profile1"
        })
        
        self.assertEqual(response.status_code, 302)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.preset_image, "profile1")
        
    @patch('cloudinary.uploader.upload')    
    def test_custom_profile_picture(self, mock_upload):
        
        mock_upload.return_value = { 
            "public_id": "test_profile_image",
            "version": 1,
            "type": "upload",
            "resource_type": "image"
        }
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        cloudinary.config(cloud_name="test-cloud")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        
        response = self.client.post('/profile/', {
            "image": image
        })
        
        self.assertEqual(response.status_code, 302)
        user.profile.refresh_from_db()
        self.assertTrue(user.profile.image)
        
    def test_change_password(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        response = self.client.post('/change_password/', {
            "old_password": "Testpassword123_",
            "new_password1": "Newpassword123_",
            "new_password2": "Newpassword123_"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/')
        user.refresh_from_db()
        self.assertTrue(user.check_password("Newpassword123_"))
        
    def test_same_password_change(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        response = self.client.post('/change_password/', {
            "old_password": "Testpassword123_",
            "new_password1": "Testpassword123_",
            "new_password2": "Testpassword123_"
        })
        
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.check_password("Testpassword123_"))
        
    def test_delete_account(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        response = self.client.post('/delete-account/', {
            "password": "Testpassword123_"
        })
        
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="testuser")
            
    def test_delete_account_invalid_password(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        self.client.login(username="testuser", password="Testpassword123_")
        
        response = self.client.post('/delete-account/', {
            "password": "Invalidpassword123_"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/')
        self.assertTrue(User.objects.filter(username="testuser").exists())
        
    def test_password_reset_page(self):
        
        response = self.client.get('/password_reset/')
        
        self.assertEqual(response.status_code, 200)
        
    def test_password_reset_valid_email(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        response = self.client.post('/password_reset/', {
            "email": "testuser@example.com"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/password_reset_done/')
        self.assertEqual(len(mail.outbox), 1)
        
    def test_password_reset_invalid_email(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        response = self.client.post('/password_reset/', {
            "email": "invalid@example.com"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/password_reset_done/')
        self.assertEqual(len(mail.outbox), 0)
        
    def test_complete_password_reset(self):
        
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Testpassword123_")
        
        response = self.client.post('/password_reset/', {
            "email": "testuser@example.com"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/password_reset_done/')
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        reset_link = email.body.split('http://testserver')[1].split()[0]
        
        response = self.client.get(reset_link)
        
        self.assertEqual(response.status_code, 302)
        set_password_url = response.url
        
        response = self.client.get(set_password_url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(set_password_url, {
            "new_password1": "Newpassword123_",
            "new_password2": "Newpassword123_"
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/password_reset_complete/')
        
        user.refresh_from_db()
        self.assertTrue(user.check_password("Newpassword123_"))
        
