#!/usr/bin/python3
from celery import shared_task
import os
from requests import post

"""
   Send Tracking SMS Notification
"""
# Configs

TRACKSEND_NG_API_KEY = os.environ.get('TRACKSEND_NG_API_KEY')
TRACKERR_TRACKING_BASE_URL = os.environ.get('TRACKERR_TRACKING_BASE_URL')

headers = {
    'content-type': 'application/json',
    'accept': 'application/json',
    'authorization': TRACKSEND_NG_API_KEY
 }

url="https://api.tracksend.co/messaging/v1/sms"


payload = {
    'from': 'KOTP',
    'country_iso_code': 'NG',
 }


@shared_task(bind=True, name='send_delivery_otp_sms')
def send_delivery_otp(self, otp, phone, country, **kwargs):
    if not country.lower() == 'nigeria':
        return

    name = kwargs['name'].split(' ')[0].title()
    parcel_number = kwargs['parcel_number'].upper()
    vendor = kwargs['vendor'].capitalize()

    payload['phone_numbers'] = [phone]
    payload['text'] = f"TrackerrGo Alert: Hello {name}, your parcel (Tracking No: {parcel_number}) from {vendor} is arriving soon.\
            Your delivery OTP is {otp}.\
            Please give this code only to the rider when he/she is with you in person. Do not share it over the phone or with anyone else."

    try:
        res = post(url, json=payload, headers=headers)
        print(res.json(), res.status_code)
    except Exception as e:
        print(e)

@shared_task(bind=True, name='send_tracking_sms')
def send_tracking_update_sms(self, phone, country, **kwargs):
    
    if not country.lower() == 'nigeria':
        return

    status = kwargs['status']
    vendor = kwargs['vendor'].capitalize()
    name = kwargs['name'].split(' ')[0].title()
    parcel_number = kwargs['parcel_number'].upper()

    payload['phone_numbers'] = [phone]

    if status.lower() == 'in transit':
        payload['text'] = f'Hello {name}, your parcel {parcel_number} from {vendor} is now in transit! You can track its progress and estimated delivery time using this link: {TRACKERR_TRACKING_BASE_URL}/{parcel_number}.'
    
    elif status.lower() == 'delivered':
        payload['text'] = f'Hello {name}, your parcel  {parcel_number} from {vendor} has been safely delivered! Thank you for your patronage.'

    elif status.lower() == 'returned':
        payload['text'] = f'Hello {name}, parcel {parcel_number} from {vendor} has been returned! Kindly reach out to {vendor} for more information about this parcel.'
    else:
        return

    try:
        res = post(url, json=payload, headers=headers)
    except Exception as e:
        print(e)
