#!/usr/bin/python3
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from user.models import User, Otp
from user.utils.generate import password_gen
from shared.celery_tasks.user_tasks.send_recovery_email import send_recovery_email
from shared.logger import setUp_logger

logger = setUp_logger(__name__, 'user.logs')

""" Route that handles password reset for a user
"""

class Recover_password(APIView):
    """ password recovery class
    """
    permission_classes = [AllowAny,]

    def get_queryset(self, email):
        user = get_object_or_404(User, email=email)
        return user


    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = self.get_queryset(email=email)
        if user:
            # generate a new password
            new_password = password_gen()
            # get the user Otp model
            try:
                user_otp_model = user.otp
                # store the password in the users otp model
                with transaction.atomic():
                    # new otp is set
                    user_otp_model.set_otp(otp=new_password)
                    user_otp_model.save()
                    # sends recovert email
                    send_recovery_email.delay(
                        email=email,
                        new_password=new_password
                        )
                    return Response({"detail": "A one time password has been sent to your email", "expiration": "10 minutes", "email": email},status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(e)
                raise ValueError('An error occurred during password reset!')        
