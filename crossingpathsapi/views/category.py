"""View module for handling requests about categories"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from crossingpathsapi.models import Category


class Categories(ViewSet):
    """Design Categories"""

    def list(self, request):
        """Handle GET requests to get all the categories
        Returns:
        Response -- JSON serialized list of categories
        """
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category
        Returns:
            Response -- JSON serialized category instance
        """
        try:
           
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for event organzier's related Django user"""
    class Meta:
        model = Category
        fields = ['id', 'label']