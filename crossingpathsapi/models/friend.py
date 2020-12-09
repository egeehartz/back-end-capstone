"""Follower model module"""
from django.db import models


class Follower(models.Model):
    """Follower database model"""
    follower = models.ForeignKey("CrossingUser", on_delete=models.CASCADE, related_name="follower")
    friend = models.ForeignKey("CrossingUser", on_delete=models.CASCADE, related_name="friend")