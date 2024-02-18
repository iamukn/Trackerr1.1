from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import UsersSerializer
from .serializers import Business_ownerSerializer
from .models import Business_owner
from user.models import User
from django.shortcuts import (get_object_or_404, get_list_or_404)


""" 
  Views to handle http methods on for Business owner
"""

class Business_ownerRegistration(APIView):
    """Views that handles the GET and POST method on 
    Business owners
    """

    parser_classes = [JSONParser,]

    def query_set(self, id, *args, **kwargs):
        # Get the user object or return a 404    
        user = get_object_or_404(User, pk=id)
        return user

    def get(self,request, *args, **kwargs):
        # This will return all Business owners information
        # That exist in the database

        # Fetch business owners model from the database
        # Serializer it and return a json response
        business_owner = get_list_or_404(Business_owner)
        business_owner_serializer = Business_ownerSerializer(business_owner, many=True)

        return Response(business_owner_serializer.data, status=status.HTTP_200_OK)


    def post(self,request, *args, **kwargs):
        # This will handle registration of business owners
        try:
            user = UsersSerializer(data=request.data)
            business_owner = Business_ownerSerializer(data={'business_name': request.data.get('business_name')})

            if business_owner.is_valid() and user.is_valid():
                user.save()
                business_owner.save(user=self.query_set(user.instance.id))
                return Response(business_owner.data, status=status.HTTP_201_CREATED)

            else:
                raise ValueError

        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
