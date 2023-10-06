from django.db import models
from django.contrib.auth.models import User
class Tier(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.CharField(max_length=100)  # Store thumbnail sizes as a comma-separated string
    allow_original_link = models.BooleanField(default=False)
    allow_expiring_link = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Image_upload/static/images/')




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    
class ExpiringLink(models.Model):
    token = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    expiration_time = models.DateTimeField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)

