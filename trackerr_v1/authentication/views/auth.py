#!/usr/bin/python3
""" Handles the token generation and email messaging"""
from django.core.mail import send_mail
from django.conf import settings
from user.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shared.logger import setUp_logger
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.test_email import emailer
import threading
import time

logger = setUp_logger(__name__, 'authentication')


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
            def worker():
                email = request.data.get('email')
                name = request.user
                name = User.objects.get(email=email).name

                try:
                    subject = "Trackerr Notification"
                    sender = settings.EMAIL_HOST_USER
                    to = [email,]
                    message = "Dear %s \n you just logged into your account on %s."% (name, time.strftime('%d-%m-%Y'))
                   #send_mail(subject, message, sender, to)
                   # test email method below
                    emailer(subject=subject, to=to, contents=message)
                except Exception as e:
                    logger.error(f"Unable to send login email {request.data.get('email')}")
                    logger.info(e)
                    pass

            threading.Thread(target=worker, daemon=True).start()

            return response
