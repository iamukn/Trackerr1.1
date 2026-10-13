#!/usr/bin/python3
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

""" Tasks that sends email """

@shared_task(bind=True, name='send_email')
def send_email(self,email, subject, message):
    data = {
        "subject": subject,
        "recipient_list": [email,],
        "message": message,
        "from_email": settings.EMAIL_SENDER,
        "fail_silently": False,
            }
    try:
        print(send_mail(**data))
        return "Email sent:"
    except Exception as e:
        return "Error sending {} email".format(subject.lower())
