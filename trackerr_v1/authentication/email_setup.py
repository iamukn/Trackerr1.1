#!/usr/bin/python3
from django.conf import settings
from authentication.logger_config import logger
from authentication.test_email import emailer
import time
""" Email messaging function """

def worker(name, email):
    email = email
    name = name

    try:
        subject = "Trackerr Notification"
        sender = settings.EMAIL_HOST_USER
        to = [email,]
        message = "Dear %s \n you just logged into your account on %s."% (name, time.strftime('%d-%m-%Y'))
        #send_mail(subject, message, sender, to)
        # test email method below
        emailer(subject=subject, to=to, contents=message)
        return 'sent'
    except Exception as e:
        logger.error(f"Unable to send login email {request.data.get('email')}")
        logger.info(e)
