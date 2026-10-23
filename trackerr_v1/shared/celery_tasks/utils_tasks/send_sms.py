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
    'callback_url': 'https://api.trackerrgo.com/api/v1/users/sms-webhook/'
 }


@shared_task(bind=True, name='send_delivery_otp_sms')
def send_delivery_otp(self, otp, phone, country, **kwargs):
    if not country.lower() == 'nigeria':
        return

    from  shared.celery_tasks.utils_tasks.reusable_sms import create_sms_record

    name = kwargs['name'].split(' ')[0].title()
    parcel_number = kwargs['parcel_number'].upper()
    vendor = kwargs['vendor'].capitalize()
    reason = kwargs['reason'].strip()

    # check if queued or sent sms already exist for this client
    exists = create_sms_record(phone=phone, reason=reason.lower())

    exists_data = exists.get('instance')
    if exists.get('exists'):
        print('Pending SMS Present for ', exists_data.receiver_phone, " with status::", exists_data.status)
        return

    payload['phone_numbers'] = [phone]

    message=f"TrackerrGo: Parcel from {vendor}. Tracking: {parcel_number}. OTP: {otp}. Share only with the rider in person."
    payload['text'] = message

    try:
        res = post(url, json=payload, headers=headers)
        #print(res.json(), res.status_code)
        res_code = res.status_code
        res_data = res.json()

        if res_code == 202:
            # creates the sms record for the phone number
            exists_data.objects.create(
                    receiver_phone=phone,
                    status=res_data.get('recipients')[0].get('status'),
                    reason = reason.lower(),
                    message=message,
                    submission_id = res_data.get('submission_id'),
                    country = country.lower(),
                    message_id = res_data.get('recipients')[0].get('message_id')
                    )
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
