#!/usr/bin/python3
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from shared.celery_tasks.emails.send_business_riders_reg_emails import send_welcome_email

"""
   Send registration email
"""

@shared_task(bind=True, name='registration_email')
def send_reg_email(self, email, username, account_type, password=""):
    try:

        send_welcome_email(
            to=email,
            username=username,
            account_type=account_type,
            password=password
                )
        return "Registration email sent"
    except Exception as e:
        print(e)
        return "Unable to send registration email"


@shared_task(bind=True, name='expo push notification')
def expo_notification(self, expo_token, customer_name, parcel_number, delivery_address):
    import requests

    payload = {'to': expo_token, 
            'data': {'order_number': parcel_number.upper(),
                'customer_name': customer_name.title(),
                'delivery_address': delivery_address.title(),
                'route': '/deliveries'}
            , 'body': f'Ready for delivery to {customer_name.title()}',
            'title': f'Dispatch: Order {parcel_number.upper()}', 'route': 'deliveries'}
    expo_url = 'https://exp.host/--/api/v2/push/send'



    res = requests.post(expo_url, json=payload)
    return customer_name
