from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import UsersSerializer
from .serializers import Business_ownerSerializer
from .models import Business_owner
from django.shortcuts import (get_object_or_404, get_list_or_404)


""" 
  Views to handle http methods on for Business owner
"""

class Business_ownerRegistration(APIView):
    """Views that handles the GET and POST method on 
    Business owners
    """

    def get(request, self, *args, **kwargs):
        # This will return all Business owners information
        # That exist in the database

        # Fetch business owners model from the database
        # Serializer it and return a json response
        business_owner = get_list_or_404(Business_owner)
        business_owner_serializer = Business_ownerSerializer(business_owner, many=True)

        return Response(business_owner_serializer.data, status=status.HTTP_200_OK)
