#!/usr/bin/python3
from celery import shared_task
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import pytz

""" Sends login email to a logged in users """

@shared_task(bind=True, name='send_login_email')
def send_login_email(self, name, email, country):
    #send email
    zone = 'Africa/Accra' if country.lower() == 'ghana' else 'Africa/Lagos'
    timezone.activate(pytz.timezone(zone))
    login_time = timezone.localtime()

    try:
        subject = "Trackerr Login!"
        sender = settings.EMAIL_HOST_USER
        to = [email,]
        message = "Hello %s, \n\n You just logged into your account on %s."% (name.title(), login_time.strftime("%I:%M %p"))
        send_mail(subject=subject, message=message, from_email=sender,recipient_list=to, fail_silently=False)
        return f'Login email sent to {to[0]}'
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
        message = "Dear %s \n\n You just changed your account password on %s."% (name.title(), login_time.strftime("%I:%M %p"))
        send_mail(subject=subject, message=message, from_email=sender,recipient_list=to, fail_silently=False)
        return f'password update email sent to {t0[0]}'
    except Exception as e:
        return 'Failed to send'
