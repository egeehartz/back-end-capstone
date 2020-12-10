""" CurrentUser ViewSet Module"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from crossingpathsapi.models import CrossingUser
from crossingpathsapi.views.crossinguser import CrossingUserSerializer

class CurrentUser(ViewSet):
    """RareUser Class"""

    def list(self, request):
        """ handles GET currently logged in user """

        #the code in the parentheses is like a WHERE clause in SQL
        user = CrossingUser.objects.get(user=request.auth.user)

        #imported the RareUserSerializer from rareuser.py to use in this module
        serializer = CrossingUserSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)