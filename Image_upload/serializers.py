from rest_framework import serializers
from .models import  Image


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField()
    exp_time = serializers.IntegerField(write_only=True)
    exp_link = serializers.BooleanField(write_only=True)

    class Meta:
        model = Image 
        fields = ['image', 'exp_time', 'exp_link']  

