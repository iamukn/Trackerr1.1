#!/usr/bin/python3
from celery import shared_task
import os
from requests import post
from .send_sms import headers, url, payload

"""
   Send Tracking SMS Notification
"""

def create_sms_record(phone: str, reason: str):

    from user.models import SMSSent as SMS

    exists =SMS.objects.filter(receiver_phone=phone, status__in=['queued'], reason=reason).first()

    return {"exists": True if exists else False, "instance": exists if exists else SMS}

@shared_task(bind=True, name='reusable_sms_sender')
def reusable_sms_sender(self, phone, country, message, reason):

    reason = reason.strip()

    # check if queued or sent sms already exist for this client
    exists = create_sms_record(phone=phone, reason=reason.lower())

    exists_data = exists.get('instance')


    if exists.get('exists'):
        print('Pending SMS Present for ', exists_data.receiver_phone, " with status::", exists_data.status)
        return

    if not country.lower() == 'nigeria':
        return


    payload['phone_numbers'] = [phone]
    payload['text'] = f"{message}"
    try:
        res = post(url, json=payload, headers=headers)
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
            print("created")
    except Exception as e:
        print('Error::',e)
