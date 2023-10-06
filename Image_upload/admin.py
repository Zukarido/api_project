from django.contrib import admin
from .models import Tier, Image, UserProfile, ExpiringLink


# Register your models here.
admin.site.register(Tier)
admin.site.register(Image)
admin.site.register(UserProfile)
admin.site.register(ExpiringLink)