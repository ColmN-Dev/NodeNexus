from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = CloudinaryField('image', default='default.png')
    preset_image = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
