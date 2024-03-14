#!/usr/bin/python3
from rest_framework.response import Response
from .password_permission import IsBusinessOrLogisticsOwner
from rest_framework import status
from .password_recovery import Recover_password
from django.shortcuts import get_object_or_404
from user.models import User

""" Change Password Feature """

class ChangePassword(Recover_password):
    ''' Route for password change for authenticated users '''
    permission_classes = [IsBusinessOrLogisticsOwner,]

    def post(self, request, *args, **kwargs):
        # Receives a post request from Logged in user for password change
        email = request.user.email
        user = self.get_queryset(email)
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
       
        if user and password1 == password2:
            user.set_password(password1)
            user.save()
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)
        
        return Response(status=status.HTTP_403_FORBIDDEN)
