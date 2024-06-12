#!/usr/bin/python3
""" Handles the token generation and email messaging"""
from django.core.mail import send_mail
from django.conf import settings
from user.models import User
from shared.celery_tasks.auth_tasks.send_email import send_login_email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from authentication.logger_config import logger
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.email_setup import worker
import threading
import time




class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    # configuring the swagger api docs

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
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            email = request.data.get('email')
            name = User.objects.get(email=email).name
            # celery email sender
            email = send_login_email.apply_async(args=[name, email], retry=False)   

            return response
