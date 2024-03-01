#!/usr/bin/python3
""" Handles the token generation and email messaging"""
from django.core.mail import send_mail
from django.conf import settings
from user.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.test_email import emailer
import threading
import time


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
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
                   # send_mail(subject, message, sender, to)
                   # test email method below
                    emailer(subject=subject, to=to, contents=message)
                except Exception as e:
                    print(e)
                    #raise ValueError('Unable to send email')

            threading.Thread(target=worker, daemon=True).start()

            return response
