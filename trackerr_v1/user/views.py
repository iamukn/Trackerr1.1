from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from .serializers import UsersSerializer
from rest_framework.views import APIView
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

