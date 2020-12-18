"""Crossing Paths User Views Module"""
import json
import uuid
import base64
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from crossingpathsapi.models import CrossingUser, Follower

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

    @action(methods=['get'], detail=False)
    def people_to_follow(self, request):

        if request.method == "GET":

            #users that are not me
            other_users = CrossingUser.objects.exclude(user=request.auth.user)

            #friends I am currently not following
            friends = Follower.objects.filter(follower_id=request.auth.user.id)

            friend_ids = []
            total_list = []

            for friend in friends:
                friend_ids.append(friend.friend.id)

            for user in other_users:
                if user.id in friend_ids:
                    pass
                else:
                     total_list.append(user)


            serializer = CrossingUserSerializer(total_list, many=True, context={'request': request})
            return Response(serializer.data)

    @action(methods=['patch'], detail=True)
    def change_profile_picture(self, request, pk=None):
        user = CrossingUser.objects.get(pk=pk)

        req_body = json.loads(request.body.decode())
        format, imgstr = req_body["profile_img"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{user.id}-{uuid.uuid4()}.{ext}')


        user.profile_img = data
        user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    

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