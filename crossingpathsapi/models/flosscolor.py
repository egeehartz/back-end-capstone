"""Floss model module"""
from django.db import models


class FlossColor(models.Model):
    """Floss database model"""
    floss_number = models.IntegerField()
    description = models.CharField(max_length=75)
    red = models.IntegerField()
    blue = models.IntegerField()
    green = models.IntegerField()
    rgb_code = models.CharField(max_length=75)
    row = models.CharField(max_length=75)