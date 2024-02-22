#!/usr/bin/python3

from django.db.models.signals import post_save
from django.dispatch import receiver
from business.models import Business_owner
from django.core.mail import send_mail
from django.conf import settings

""" 
    Signals to send emails as soon as a User is Created
"""

@receiver(post_save, sender=Business_owner)
def send_welcome_email(sender, instance, created, **Kwargs):

    if created:# only send email for new users

        subject = 'Welcome to Trackerr!!'
        message = f'Hello {instance.user.name}, you account has been successfully regisitered and you are set to start tracking your parcels in realtime ;)'
        from_email = settings.EMAIL_HOST_USER 
        to = [instance.user.email,]
        try:
            send_mail(subject, message, from_email, to)
        except Exception:
        # Write a logging for this incase an exception occurs
            print('ERROR IN BUSINESS SIGNALS, Please check!!')
