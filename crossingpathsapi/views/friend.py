from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.fields import NullBooleanField
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework import status
from crossingpathsapi.models import Follower, CrossingUser
from datetime import date


class Follows(ViewSet):

    def list(self, request):

        followings = Follower.objects.all()

        #set variables
        follower_user_id = self.request.query_params.get('follower_id', None)
        friend_user_id = self.request.query_params.get('friend_id', None)


        #get friends by any follower
        if follower_user_id is not None:
            followings = followings.filter(follower_id=follower_user_id)
        
        #get followers by any friend
        if friend_user_id is not None:
            followings = followings.filter(friend_id=friend_user_id)

        serializer = FollowerSerializer(
            followings, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):

        new_following = Follower()

        #current user
        user = CrossingUser.objects.get(user=request.auth.user)
        new_following.follower = user

        #friend they want to follow
        new_following.friend = CrossingUser.objects.get(pk=request.data["friendId"])

        new_following.save()

        serializer = FollowerSerializer(new_following, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single category
        Returns:
            Response -- 200, 404, or 500 status code
        """


        try:
            following = Follower.objects.get(pk=pk)
            following.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Follower.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FollowerCrossingUserSerializer(serializers.ModelSerializer):
    """Serializer for RareUser Info from a post"""
    class Meta:
        model = CrossingUser
        fields = ('id', 'full_name', 'username', 'profile_img')

class FollowerSerializer(serializers.ModelSerializer):
    follower = FollowerCrossingUserSerializer(many=False)
    friend = FollowerCrossingUserSerializer(many=False)

    class Meta:
        model = Follower
        fields = ('id', 'friend', 'follower')
        depth = 1