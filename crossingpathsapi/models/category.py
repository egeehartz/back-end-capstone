"""Category model module"""
from django.db import models


class Category(models.Model):
    """Category database model"""
    label = models.CharField(max_length=25)
