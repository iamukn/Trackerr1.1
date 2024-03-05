#!/usr/bin/python3
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.models import User
from user.generate import password_gen
from authentication.test_email import emailer
from threading import Thread

""" Route that handles password reset for a user
"""

class Recover_password(APIView):
    """ password recovery class
    """
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
                
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_200_OK)
            except Exception:
                raise ValueError('An error occurred during password reset!')        
