"""Crossing Paths User Views Module"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from crossingpathsapi.models import CrossingUser

class CrossingUsers(ViewSet):
    """CrossingUser Class"""

    def list(self, request):
        """ handles GET all"""
        users = CrossingUser.objects.all()

        serializer = CrossingUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
       
        try:
            user = CrossingUser.objects.get(pk=pk)
            
            #logic to set an unmapped property on CrossingUser 
            #will let front end determine if the user retrieved by this function is the current user
            if request.auth.user.id == int(pk):
                user.is_current_user = True
            else:
                user.is_current_user = False

            serializer = CrossingUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class CrossingUserSerializer(serializers.ModelSerializer):
    """Serializer for CrossingUser Info from a post"""
    user = UserSerializer(many=False)

    class Meta:
        model = CrossingUser
        fields = ('id', 'user', 'profile_img', 'is_current_user')