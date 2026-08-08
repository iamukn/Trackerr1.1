#!/usr/bin/python3
from celery import shared_task
import os
from requests import post

"""
   Send Tracking SMS Notification
"""

@shared_task(bind=True, name='send_tracking_sms')
def send_tracking_update_sms(self, phone, country, **kwargs):
    
    if not country.lower() == 'nigeria':
        return

    TRACKSEND_NG_API_KEY = os.environ.get('TRACKSEND_NG_API_KEY')
    TRACKERR_TRACKING_BASE_URL = os.environ.get('TRACKERR_TRACKING_BASE_URL')
    status = kwargs['status']
    vendor = kwargs['vendor'].capitalize()
    name = kwargs['name'].split(' ')[0].title()
    parcel_number = kwargs['parcel_number'].upper()

    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': TRACKSEND_NG_API_KEY
            }

    payload = {
        'from': 'KOTP',
        'phone_numbers': [phone],
        'country_iso_code': 'NG',
            }

    if status.lower() == 'in transit':
        payload['text'] = f'Hello {name}, your parcel {parcel_number} from {vendor} is now in transit! You can track its progress and estimated delivery time using this link: {TRACKERR_TRACKING_BASE_URL}/{parcel_number}.'
    
    elif status.lower() == 'delivered':
        payload['text'] = f'Hello {name}, your parcel  {parcel_number} from {vendor} has been safely delivered! Thank you for your patronage.'

    elif status.lower() == 'returned':
        payload['text'] = f'Hello {name}, parcel {parcel_number} from {vendor} has been returned! Kindly reach out to {vendor} for more information about this parcel.'
    else:
        return



    url="https://api.tracksend.co/messaging/v1/sms"

    try:
        res = post(url, json=payload, headers=headers)
    except Exception as e:
        print(e)
