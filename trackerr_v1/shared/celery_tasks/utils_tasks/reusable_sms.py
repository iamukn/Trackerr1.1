#!/usr/bin/python3
from celery import shared_task
import os
from requests import post
from .send_sms import headers, url, payload

"""
   Send Tracking SMS Notification
"""
@shared_task(bind=True, name='reusable_sms_sender')
def reusable_sms_sender(self, phone, country, message):
    if not country.lower() == 'nigeria':
        return

    payload['phone_numbers'] = [phone]
    payload['text'] = f"{message}"
    try:
        res = post(url, json=payload, headers=headers)
        print(res.json(), res.status_code)
    except Exception as e:
        print('Error::',e)
