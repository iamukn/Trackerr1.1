#!/usr/bin/python3
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .password_permission import IsBusinessOrLogisticsOwner
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from shared.celery_tasks.auth_tasks.send_email import send_update_email
from shared.logger import setUp_logger
from .password_recovery import Recover_password
from django.shortcuts import get_object_or_404
from user.utils.shortcuts import get_otp_or_none
from django.db import transaction
from user.models import Otp

# logger
logger = setUp_logger(__name__, 'business.logs')

""" Change Password Feature """

class ChangePassword(Recover_password):
    ''' Route for password change for authenticated users '''
    permission_classes = [IsBusinessOrLogisticsOwner,]
    
    # swagger docs
    @swagger_auto_schema(
        operation_summary='Change a users password',
        operation_description='POST Endpoint that updates the user password',
        tags=['Users'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password1': openapi.Schema(type=openapi.TYPE_STRING, title='password1', description='password'),
                'password2': openapi.Schema(type=openapi.TYPE_STRING, title='password2', description='confirm password'),
                },
            example={
                'password1': 'hellow0rlD',
                'password2': 'hellow0rlD',
                }
            ),
        responses={
            '206': openapi.Response(
                type=openapi.TYPE_OBJECT,
                description='password updated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='password updated successfully')
                        },
                    example={
                        'message': 'password updated successfully'
                        }
                    )
                ),
            '400': openapi.Response(
                description='Error: Bad Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='passwords must match')
                        },
                    example={
                        'error': 'passwords must match'
                        }
                    )
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided.')
                        },
                    example={
                        'detail': 'Authentication credentials were not provided.'
                        }
                    )
                ),
            }
            )
    def post(self, request, *args, **kwargs):
        # Receives a post request from Logged in user for password change
        email = request.user.email
        user = self.get_queryset(email)
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
       
        if user:
            if password1 == password2:
                with transaction.atomic():
                    user.set_password(password1)
                    user.save()
                    return Response({'message': 'password updated successfully'}, status=status.HTTP_206_PARTIAL_CONTENT)
            return Response({"error": "passwords must match"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": f"{email} not found"},status=status.HTTP_400_BAD_REQUEST)

class UpdatePassword(Recover_password):
    """ Route for password change for reset password endpoints """
    
    permission_classes = [AllowAny,]
    # Swagger docs
    @swagger_auto_schema(
        operation_description='updates a password for a user',
        operation_summary='POST Endpoint to update password',
        tags=['Users'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='one time password'),
                'password1': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
                'password2': openapi.Schema(type=openapi.TYPE_STRING, description='confirm password'),
                },
            example={
                'otp': '23456789',
                'password1': 'h3ll0W0rlD',
                'password2': 'h3ll0W0rlD',
                }
            ),
        responses={
            '200': openapi.Response(
                description='Password changed successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='password updated successfully')
                        },
                    example={
                        'message': 'password updated successfully'
                        }
                    )
                ),
            }
            )
    # handles the post request
    def post(self, request, *args, **kwargs):
        # retrieve data from the request object
        otp = request.data.get('otp')
        #email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        # get user
        #user = self.get_queryset(email)
        # get otp owner
        otp_owner = get_otp_or_none(otp=otp, model=Otp)

        if otp_owner:
            if password1 != password2:
                return Response({"error": "password must match!"}, status=status.HTTP_400_BAD_REQUEST)
            user_otp = otp_owner
            # check if the otp is still valid
            if user_otp.hashed_otp == None:
                return Response({"error": "otp doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            if user_otp.check_otp(otp=str(otp)):
                with transaction.atomic():
                    # set password
                    user = user_otp.owner
                    user.set_password(password1)
                    user.save()
                    # reset the otp
                    user_otp.hashed_otp = None
                    user_otp.save()
                    #send update email
                    try:
                        send_update_email.delay(email=user.email, name=user.name)
                        return Response({"message":"password updated successfully"}, status=status.HTTP_200_OK)
                    except Exception as e:
                        logger.error(f"Failed to enqueue email task: {str(e)}")
            return Response({"error": "incorrect or expired otp"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": f"otp does not exist"}, status=status.HTTP_404_NOT_FOUND)
