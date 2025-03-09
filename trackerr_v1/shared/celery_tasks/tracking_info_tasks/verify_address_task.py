#!/usr/bin/python3
from celery import shared_task
from django.conf import settings
from tracking_information.utils.validate_shipping_address import verify_address
""" Tasks that sends recovery email """

@shared_task(bind=True, name='verify shipping address')

def verify_shipping_address(self, address:str):
    try:
        addr = verify_address(address=address)
        return addr
    except IndexError as e:
        return {'error': 'address not found'} 
