"""View module for handling requests about posts"""
from datetime import date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from crossingpathsapi.models import CrossingUser, Design, Category, crossinguser, design


class Designs(ViewSet):

    def list(self, request):

        designs = Design.objects.all()   

        #set unmapped property in the design model
        for design in designs:

            design.created_by_current_user = None

            if design.user.id == request.auth.user.id:
                design.created_by_current_user = True
            else:
                design.created_by_current_user = False

        #set variables
        user_id = self.request.query_params.get('user_id', None)
        category_id = self.request.query_params.get('category_id', None)
        
        #filter by user_id /designs?user_id=2
        if user_id is not None:
            designs = designs.filter(user_id=user_id)

        #filter by category /designs?category_id=1
        if category_id is not None:
            designs = designs.filter(category_id=category_id)

        serializer = DesignSerializer(
            designs, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # get by id /designs/2
            design = Design.objects.get(pk=pk)

            #set unmapped property
            if design.user.id == request.auth.user.id:
                design.created_by_current_user = True
            else:
                design.created_by_current_user = False

            #serialize    
            serializer = DesignSerializer(design, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post instance
        """
        user = request.auth.user
        design = Design()

        try:
            design.design_img = request.data["designImage"]
            design.link = request.data["link"]
            design.title = request.data["title"]
            design.public = request.data["public"]
            design.created_on = request.data["createdOn"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        design.user_id = user.id

        try:
            category = Category.objects.get(pk=request.data["categoryId"])
            design.category_id = category.id
        except Category.DoesNotExist as ex:
            return Response({'message': 'Design type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None:
            try:
                design.save()
                serializer = DesignSerializer(design, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for posts"""
       
        crossinguser = CrossingUser.objects.get(user=request.auth.user)

        design = Design.objects.get(pk=pk)
        design.design_img = request.data["designImage"]
        design.link = request.data["link"]
        design.title = request.data["title"]
        design.public = request.data["public"]
        design.created_on = request.data["createdOn"]
        design.user = crossinguser

        category = Category.objects.get(pk=request.data["categoryId"])
        design.category = category
        design.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            design = Design.objects.get(pk=pk)
            design.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Design.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DesignCrossingUserSerializer(serializers.ModelSerializer):
    """Serializer for RareUser Info from a post"""
    class Meta:
        model = CrossingUser
        fields = ('id', 'user', 'full_name')

class DesignSerializer(serializers.ModelSerializer):
    """Basic Serializer for a post"""
    user = DesignCrossingUserSerializer(many=False)

    class Meta:
        model = Design
        fields = ('id', 'title', 'design_img', 'link',
                  'user', 'category_id', 'category', 'public', 
                  'created_on', 'created_by_current_user')
        depth = 1