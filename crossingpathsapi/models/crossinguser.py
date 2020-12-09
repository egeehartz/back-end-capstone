"""RareUser Model Module"""
from django.db import models
from django.contrib.auth.models import User

class CrossingUser(models.Model):
    """CrossingUser Model"""
    profile_image_url = models.ImageField(upload_to="images/", blank='true', null='true')
    user = models.OneToOneField(User, on_delete=models.CASCADE)