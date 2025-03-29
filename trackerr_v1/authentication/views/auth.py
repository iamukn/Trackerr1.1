#!/usr/bin/python3
""" Handles the token generation and email messaging"""
from django.core.mail import send_mail
from django.conf import settings
from user.models import User
from user.views.password_permission import IsBusinessOrLogisticsOwner
from shared.celery_tasks.auth_tasks.send_email import send_login_email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from authentication.logger_config import logger
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
import time
from authentication.serializers import CustomTokenObtainPairSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    
    @swagger_auto_schema(
        operation_summary='Handle user login and send a notification email upon successful login.',
        operation_description='POST /login',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, title='Email', minLength=1),
                'password': openapi.Schema(type=openapi.TYPE_STRING, title='Password', minLength=1),
                },
            example={
                'email': 'testuser@gmail.com',
                'password': 'password'
                },
            required=['email', 'password']
            ),
        responses={
            '200': openapi.Response(
                description='Login Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(
                            title='access token',
                            description='generated access token',
                            type=openapi.TYPE_STRING,
                            ),
                        'refresh': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title='refresh token',
                            description='generated refresh token'
                            ),
                        'id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title='id',
                            description='unique ID of the logged in user'
                            ),
                        'account_type': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['admin', 'business', 'rider'],
                            title='account type',
                            description='specifies the type of account type which can be either admin, business or rider',
                            )
                        },
                    example={
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczODQ0MTg1NCwiaWF0IjoxNzMzMjU3ODU0LCJqdGkiOiI2YzVkYTg2OWZkYjI0YjIwOWEwOGYxM2E4ZDhlNGYwMSIsInVzZXJfaWQiOjc3fQ.unYFZ6CvkVFgYjleHrw_7TJFh5cnOgTS8LJWG4dYFZU",
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMjYxNDU0LCJpYXQiOjE3MzMyNTc4NTQsImp0aSI6ImVjZmExYjE1NDg0MTQzZDk4MmI1YWU4OTJjNzM5YzMyIiwidXNlcl9pZCI6Nzd9.UaMQrDAtY4ULXW3AFuF-0ABsZcnfpxFg0dHOvjRvyUY",
                        "id": 75
                        }
                    ),
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, title='error message', description='No active account with the given credentials'),
                        },
                    example={
                     "detail": "No active account found with the given credentials"
                    }
                    )
                )
            }
            )
    def post(self, request, *args, **kwargs):
        """
            Handle user login and send a notification email upon successful login.

            POST /login

            Parameters:
              - request (HttpRequest): The HTTP request object containing login data with 'email' and 'password'.
              - *args: Additional positional arguments.
              - **kwargs: Additional keyword arguments.

            Returns:
              - HttpResponse: Response object with login result, including refresh and access tokens.

              Sends a login notification email to the user asynchronously if login is successful.
        """
        # converts the email to lowercase
        data = request.data.copy()
        
        if 'email' in data:
            data['email'] = data['email'].lower()

        request.__full_data = data
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            email = request.data.get('email').lower()
            name = User.objects.get(email=email).name
            # sends a login email to the user
            email = send_login_email.apply_async(args=[name, email], retry=False)   

            return response
