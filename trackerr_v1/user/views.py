from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from .models import User
from .serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
"""
Views for the user application
"""

class UsersView(APIView):
    ''' Method to handle all the http methods on the
    User model
    '''

    def queryset(self):
        """Method that gets the User models datas
        """
        return User.objects.all()

    def get(self, request, *args, **kwargs):

        """ Handles the get requests on the users endpoint
        """

        users = self.queryset()
        serializer = UsersSerializer(users, many=True)

        return Response(serializer.data, status='200')


class UserView(UsersView):
    """ Endpoint to handle individual user data update 
        The parser_class helps to handle the image field in the serializer
    """
    parser_classes = (MultiPartParser, JSONParser)

    def get(self, request, pk,  *args, **kwargs):
        user = self.queryset().get(id=pk)
        serializer = UsersSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk,  *args, **kwargs):

        user = self.queryset().get(id=pk)
        serializer = UsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status.HTTP_206_PARTIAL_CONTENT)

        return Response(status.HTTP_404_NOT_FOUND)

