from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from user.models import User
from user.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from business.serializers import Business_ownerSerializer


"""
Views for the user application
"""

class UsersView(APIView):
    ''' Method to handle all the http methods on the
    User model
    '''
    permission_classes = [IsAdminUser,]
    parser_classes = (JSONParser,)

    def queryset(self):
        """Method that gets the User models datas
        """
        return User.objects.all()
    
    # Swagger documentation
    @swagger_auto_schema(
            operation_description='Retrieves all registered users data',
            operation_summary='GET all registered users data',
            tags=['Users'],
            responses={
                '200': openapi.Response(
                    description='Successful',
                    schema=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='unique userID of user'),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description='name of user'),
                                'email': openapi.Schema(type=openapi.TYPE_STRING, description='users email'),
                                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone number of user'),
                                'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='verification status of user'),
                                'account_type': openapi.Schema(type=openapi.TYPE_STRING, description='account type'),
                                'address': openapi.Schema(type=openapi.TYPE_STRING, description='address of user'),
                                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='active status of user'),
                                'created_on': openapi.Schema(type=openapi.TYPE_STRING, description='when the user was created'),
                                'updated_on': openapi.Schema(type=openapi.TYPE_STRING, description='users profile update time or null'),
                                'avatar': openapi.Schema(type=openapi.TYPE_STRING, description='users profile picture link or an empty string'),
                                },
                            example = {
                                'id': 1,
                                "name": "stone cold",
                                "email": "user@example.com",
                                "phone_number": "4567890987678",
                                "is_verified": True,
                                "account_type": "business",
                                "address": "string",
                                "is_active": True,
                                "created_on": "2024-11-22T21:53:44.274771Z",
                                "updated_on": "2024-11-22T21:51:54.113000Z",
                                "avatar": ""
                                }
                            )
                        )
                    ),
                '401': openapi.Response(
                    description='Error: Unauthorized',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'detail': openapi.Schema(type=openapi.TYPE_STRING, title='unauthorized', description='Authentication credentials were not provided.')
                            },
                        example={
                            'detail': 'Authentication credentials were not provided.'
                            }
                        ),
                    ),
                '403': openapi.Response(
                    description='Error: Forbidden',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'detail': openapi.Schema(type=openapi.TYPE_STRING, title='forbidden', description='You do not have permission to perform this action.')
                                },
                        example={
                            'detail': 'You do not have permission to perform this action.'
                                 }
                        ),
                    )
                }
            )
    # Retrieve all users
    def get(self, request, *args, **kwargs):

        """ Returns all registered users
        """
            
        users = self.queryset()
        serializer = UsersSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserView(UsersView):
    """ Endpoint to handle individual user data update 
        The parser_class helps to handle the image field in the serializer
    """
    permission_classes = [ IsAuthenticated,]
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
