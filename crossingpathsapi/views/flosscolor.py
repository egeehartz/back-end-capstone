"""View module for handling requests about categories"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from crossingpathsapi.models import FlossColor 


class FlossColors(ViewSet):
    """Design Categories"""

    def list(self, request):
        """Handle GET requests to get all the categories
        Returns:
        Response -- JSON serialized list of categories
        """
        colors = FlossColor.objects.all()

        serializer = FlossColorSerializer(
            colors, many=True, context={'request': request})
        return Response(serializer.data)


class FlossColorSerializer(serializers.ModelSerializer):
    """JSON serializer for event organzier's related Django user"""
    class Meta:
        model = FlossColor
        fields = ['id', 'floss_number', 'description', 'rgb_code']