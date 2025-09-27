#!/usr/bin/python3
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

"""
   Send registration email
"""

@shared_task(bind=True, name='registration_email')
def send_reg_email(self, email, username, account_type, password=""):

    subject = 'Welcome to Trackerr!!'

    message = f'Hello {username}, your {account_type} account has been successfully created and you are set to start generating and tracking your parcels in realtime;)' if account_type == 'business' \
            else"""
                Hi {username},
                
                Your {account_type} account has been created successfully.
                Here are your login credentials:
                Email: {email}
                Password: {password}
                Please log in and change your password immediately for security reasons.
                
                Regards,
                Trackerr Team
            """.format(username=username, email=email[0], password=password, account_type=account_type)
    from_email = settings.EMAIL_HOST_USER
    recipient_email = email

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_email,
            fail_silently = False,
                )
        return "Registration email sent"
    except Exception as e:
        print(e)
        return "Unable to send registration email"
