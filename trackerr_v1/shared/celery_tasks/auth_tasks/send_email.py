#!/usr/bin/python3
from celery import shared_task
import time
from django.core.mail import send_mail
from django.conf import settings

""" Sends login email to a logged in users """

@shared_task(bind=True, name='send_login_email')
def send_login_email(self, name, email):
    #send email
    try:
        subject = "Trackerr Login!"
        sender = settings.EMAIL_HOST_USER
        to = [email,]
        message = "Dear %s \n you just logged into your account on %s."% (name, time.strftime('%d-%m-%Y'))
        send_mail(subject=subject, message=message, from_email=sender,recipient_list=to, fail_silently=False)
        return 'Login email sent '
    except Exception:
        return 'Failed to send'
    
