"""CrossingUser Model Module"""
from django.db import models
from django.contrib.auth.models import User

class CrossingUser(models.Model):
    """CrossingUser Model"""
    profile_img = models.ImageField(upload_to="images/", blank='true', null='true')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def is_current_user(self):
        return self.__is_current_user

    @is_current_user.setter
    def is_current_user(self,value):
        self.__is_current_user = value