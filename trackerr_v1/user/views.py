from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from .models import User
from .serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from business.serializers import Business_ownerSerializer


"""
Views for the user application
"""

class UsersView(APIView):
    ''' Method to handle all the http methods on the
    User model
    '''
    parser_classes = (JSONParser,)

    def queryset(self):
        """Method that gets the User models datas
        """
        return User.objects.all()

    def get(self, request, *args, **kwargs):

        """ Handles the get requests on the users endpoint
        """
            
        users = self.queryset()
        serializer = UsersSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        try:

            user_serializer = UsersSerializer(data=request.data)
            
            if user_serializer.is_valid():
                user_serializer.save()

        except Exception:
            raise ValueError

        if request.data.get('account_type') == 'business':            
            user = User.objects.get(email=request.data.get('email'))
            business_serializer = Business_ownerSerializer(data={'business_name': request.data.get('business_name')})
            if business_serializer.is_valid():
                business_serializer.save(user=user)
                return Response(business_serializer.data, status=status.HTTP_201_CREATED)
            return Response(business_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.data.get('account_type') == 'logistics':
            pass

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserView(UsersView):
    """ Endpoint to handle individual user data update 
        The parser_class helps to handle the image field in the serializer
    """
    parser_classes = (JSONParser,)

    def get(self, request, pk,  *args, **kwargs):
        try:
            user = self.queryset().get(id=pk)
            serializer = UsersSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk,  *args, **kwargs):
        try:
            user = self.queryset().get(id=pk)
            serializer = UsersSerializer(user, data=request.data, partial=True)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status.HTTP_206_PARTIAL_CONTENT)
        return Response(status.HTTP_404_NOT_FOUND)

