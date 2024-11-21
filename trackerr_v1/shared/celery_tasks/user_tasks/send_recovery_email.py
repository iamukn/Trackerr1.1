#!/usr/bin/python3
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

""" Tasks that sends recovery email """

@shared_task(bind=True, name='send_recovery_email')
def send_recovery_email(self,email, new_password):
    data = {
        "subject": "Password reset",
        "recipient_list": [email,],
        "message": "Your OTP is %(password)s" %{'password': new_password},
        "from_email": settings.EMAIL_HOST_USER,
        "fail_silently": False,
            }
    try:
        send_mail(**data)
        return "Password recovery email has been sent"
    except Exception as e:
        return "Error sending recovery email"
