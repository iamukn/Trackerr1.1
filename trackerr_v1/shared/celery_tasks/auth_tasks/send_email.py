#!/usr/bin/python3
from celery import shared_task
from authentication.email_setup import worker

""" Sends login email to a logged in users """

@shared_task(bind=True)
def send_login_email(self, name, email):
    #send email
    try:
        worker(name=name, email=email)
        return 'Login email sent '
    except Exception:
        return 'Failed to send'
    
