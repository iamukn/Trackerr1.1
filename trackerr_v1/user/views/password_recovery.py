#!/usr/bin/python3
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from user.models import User
from user.utils.generate import password_gen
from authentication.test_email import emailer
from threading import Thread
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
            new_password = password_gen()
            try:
                Thread(target=emailer, kwargs={"subject":'Password reset','to':email, 'contents':'Your OTP is %s'%new_password}, daemon=True).start()
                
                with transaction.atomic():
                    user.set_password(str(new_password))
                    user.save()
                    return Response("{'detail': 'A one time password has been sent to you email'}",status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(e)
                raise ValueError('An error occurred during password reset!')        
