from django.shortcuts import render
from django.db.transaction import atomic
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from user.models import User
from user.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
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

    class CustomPaginator(PageNumberPagination):
        page_size = 10  # Number of items per page
        page_size_query_param = 'page_size'  # Allow client to set page size
        max_page_size = 100  # Maximum allowed page size

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
            
        users = self.queryset().order_by('-date_joined')
                # Apply pagination
        paginator = self.CustomPaginator()
        paginated_queryset = paginator.paginate_queryset(users, request)

        serializer = UsersSerializer(paginated_queryset, many=True)
                # Return paginated response
        return paginator.get_paginated_response(serializer.data)        
    
class UserView(UsersView):
    """ Endpoint to handle individual user data update 
        The parser_class helps to handle the image field in the serializer
    """
    permission_classes = [ IsAdminUser,]
    parser_classes = (JSONParser,)
    
    # swagger documentation
    @swagger_auto_schema(
        operation_summary='GET information of a user using ID',
        operation_description='Returns profile information of a user using its ID',
        tags=['Users'],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                required=True
                )
            ],
        responses={
            '200': openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_NUMBER, description='users unique ID'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='users name'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='users email'),
                        'phone_number':openapi.Schema(type=openapi.TYPE_STRING, description='users phone number'),
                        'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='verification status or null'),
                        'account_type': openapi.Schema(type=openapi.TYPE_STRING, description='account type'),
                        'address':openapi.Schema(type=openapi.TYPE_STRING, description='users address'),
                        'is_active':openapi.Schema(type=openapi.TYPE_BOOLEAN, description='account status or null'), 
                        'created_on': openapi.Schema(type=openapi.TYPE_STRING, description='account creation date'),
                        'updated_on': openapi.Schema(type=openapi.TYPE_STRING, description='last profile update date'),
                        'avatar':openapi.Schema(type=openapi.TYPE_STRING, description='profile picture url')
                        },
                    example = {
                        "id": 21,
                        "name": "ukaegb21",
                        "email": "ukaegb102112@gmail.com",
                        "phone_number": "+23412167610",
                        "is_verified": False,
                        "account_type": "business",
                        "address": "36b authority avenue",
                        "is_active": True,
                        "created_on": "2024-11-18T23:15:19.707081Z",
                        "updated_on": None,
                        "avatar": ""
                    }
                    ),
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example={
                        'detail': "Authentication credentials were not provided."
                        }
                    )
                ),
            '403': openapi.Response(
                description='Error: Forbidden',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example={
                        'detail': 'You do not have permission to perform this action.'
                        }
                    ),
                ),
            '404': openapi.Response(
                description='Error: Not Found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                         },
                    example={
                        'detail': "user does not exist"
                         }
                    ),
                ),
            }
            )
    def get(self, request, pk,  *args, **kwargs):
        """ Returns information about a user 
            This endpoint is open to ADMIN users only
        """
        try:
            user = self.queryset().get(id=pk)
            serializer = UsersSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'user does not exist'},status=status.HTTP_404_NOT_FOUND)

    # swagger documentation
    @swagger_auto_schema(
        operation_summary='Partial Update information of a user using ID',
        operation_description='Partially update profile information of a user using its ID',
        tags=['Users'],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                required=True
                )
            ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='users new name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='new email address'),
                'phone_number':openapi.Schema(type=openapi.TYPE_STRING, description='users phone number'),
                'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='verification status or null'),
                'account_type': openapi.Schema(type=openapi.TYPE_STRING, description='account type'),
                'is_active':openapi.Schema(type=openapi.TYPE_BOOLEAN, description='account status or null'),
                }
            ),
        responses={
            '200': openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_NUMBER, description='users unique ID'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='users name'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='users email'),
                        'phone_number':openapi.Schema(type=openapi.TYPE_STRING, description='users phone number'),
                        'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='verification status or null'),
                        'account_type': openapi.Schema(type=openapi.TYPE_STRING, description='account type'),
                        'address':openapi.Schema(type=openapi.TYPE_STRING, description='users address'),
                        'is_active':openapi.Schema(type=openapi.TYPE_BOOLEAN, description='account status or null'),
                        'created_on': openapi.Schema(type=openapi.TYPE_STRING, description='account creation date'),
                        'updated_on': openapi.Schema(type=openapi.TYPE_STRING, description='last profile update date'),
                        'avatar':openapi.Schema(type=openapi.TYPE_STRING, description='profile picture url')
                        },
                    example = {
                        "id": 21,
                        "name": "ukaegb21",
                        "email": "ukaegb102112@gmail.com",
                        "phone_number": "+23412167610",
                        "is_verified": False,
                        "account_type": "business",
                        "address": "36b authority avenue",
                        "is_active": True,
                        "created_on": "2024-11-18T23:15:19.707081Z",
                        "updated_on": None,
                        "avatar": ""
                    }
                    ),
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example={
                        'detail': "Authentication credentials were not provided."
                        }
                    )
                ),
            '403': openapi.Response(
                description='Error: Forbidden',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example={
                        'detail': 'You do not have permission to perform this action.'
                        }
                    ),
                ),
            '404': openapi.Response(
                description='Error: Not Found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                         },
                    example={
                        'detail': "user does not exist"
                         }
                    ),
                ),
            }
            )
    def put(self, request, pk,  *args, **kwargs):
        try:
            with atomic():
                user = self.queryset().get(id=pk)
                serializer = UsersSerializer(user, data=request.data, partial=True)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    # Swagger documentation
    @swagger_auto_schema(
        operation_description="Deletes a user | Administrators only",
        operation_summary="Endpoint that deletes a user",
        tags=['Users'],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                required=True
                )
            ],
        responses={
            '204': openapi.Response(
                description='No Content',
                ),
            '401': openapi.Response(
                description="Error: Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example = {'detail':"Authentication credentials were not provided."}
                    )
                ),
            '403': openapi.Response(
                description="Error: Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example={
                        'detail': 'You do not have permission to perform this action.'
                        }
                    ),
                ),
            '404': openapi.Response(
                description='Error: Not Found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example = {'detail':'user does not exist'}
                    )
                )
            }
            )
    def delete(self, request, pk, *args, **kwargs):
        if not request.user:
            return Response({'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            #fetches the user from the Users model and deletes it
            user = User.objects.get(id=pk)
            user.delete()
            
            #ADD A FUNCTIONALITY THAT EMAILS THE USER THAT THEIR ACCOUNT HAS JUST BEEN DELETED
            return Response({'status': 'user deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response({'detail': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
