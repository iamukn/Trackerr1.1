#!/usr/bin/python3
from celery import shared_task
from datetime import datetime
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
        message = "Dear %s \n you just logged into your account on %s."% (name, datetime.now().strftime('%d-%m-%Y at %H:%M:%S PM'))
        send_mail(subject=subject, message=message, from_email=sender,recipient_list=to, fail_silently=False)
        return 'Login email sent to {t0[0]}'
    except Exception as e:
        return 'Failed to send'
    
""" Notify customer of a sucessful password reset """
@shared_task(bind=True, name='send_update_email')
def send_update_email(self, name, email):
    #send email
    try:
        subject = "PASSWORD UPDATED SUCCESSFULLY!"
        sender = settings.EMAIL_HOST_USER
        to = [email,]
        message = "Dear %s \n you just changed your account password on %s."% (name, datetime.now().strftime('%d-%m-%Y at %H:%M:%S PM'))
        send_mail(subject=subject, message=message, from_email=sender,recipient_list=to, fail_silently=False)
        return 'Login email sent to {t0[0]}'
    except Exception as e:
        return 'Failed to send'
