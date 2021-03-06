"""Design model module"""
from django.db import models

class Design(models.Model):
    """Design database model"""

    user = models.ForeignKey("CrossingUser", on_delete=models.CASCADE, related_name="crossinguser")
    design_img = models.ImageField(upload_to="images/", blank='true', null='true')
    link = models.CharField(max_length=256, null='true')
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null = True, related_name="category")
    title = models.CharField(max_length=75)
    public = models.BooleanField(default=False)
    created_on = models.DateField()

    @property
    def created_by_current_user(self):
        return self.__created_by_current_user

    @created_by_current_user.setter
    def created_by_current_user(self, value):
        self.__created_by_current_user = value

    @property
    def created_by_friend(self):
        return self.__created_by_friend

    @created_by_friend.setter
    def created_by_friend(self, value):
        self.__created_by_friend = value