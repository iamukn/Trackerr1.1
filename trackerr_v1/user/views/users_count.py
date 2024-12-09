#!/usr/bin/python3
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from user.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

""" View that returns the count of all users """

class Users_count(APIView):
    """ Fetches the count of all the users"""
    permission_classes = [IsAdminUser]
    
    # swagger documentation
    @swagger_auto_schema(
        operation_description='Retrieves the total of all users',
        operation_summary='GET total users',
        tags=['Users'],
        responses={
            '200': openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_users': openapi.Schema(type=openapi.TYPE_INTEGER, title='total users', description='count of all users')
                        },
                    example={
                        'total_users': 42,
                        }
                    )
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, title='unauthorized', description='Authentication credentials were not provided.')
                        }
                    ,
                    example={
                        'detail': 'Authentication credentials were not provided.'
                        }
                    )
                ),
            '403': openapi.Response(
                description='Error: Forbidden',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, title='forbidden', description='You do not have permission to perform this action.')
                         }
                       ,
                       example={
                           'detail': 'You do not have permission to perform this action.'
                           }
                       )
                ),
            }
            )
    # Retrieve count of all users
    def get(self, request, *args, **kwargs) -> int:
        # fetches the user and returns its count

        count = User.objects.values('email').count()
        return Response({'total_users':count}, status=status.HTTP_200_OK)
