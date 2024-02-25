from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from user.models import User
from user.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    

class UserView(UsersView):
    """ Endpoint to handle individual user data update 
        The parser_class helps to handle the image field in the serializer
    """
    permission_classes = [IsAuthenticated,]
    parser_classes = (JSONParser,)

    def get(self, request, pk,  *args, **kwargs):
        try:
            print(request.user, request.auth)
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

    def delete(self, request, pk, *args, **kwargs):

        if not request.user:
            return Response({'status': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)

        try:
            #fetches the user from the Users model and deletes it
            user = User.objects.get(id=pk)
            user.delete()
            
            #ADD A FUNCTIONALITY THAT EMAILS THE USER THAT THEIR ACCOUNT HAS JUST BEEN DELETED
            return Response({'status': 'Account successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response({'status': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)


class Users_count(APIView):
    """ Fetches the count of all the users"""
    permissions_classes = [AllowAny]

    def get(self, request, *args, **kwargs) -> int:
        # fetches the user and returns its count

        count = User.objects.all().count()
        return Response(count, status=status.HTTP_200_OK)
