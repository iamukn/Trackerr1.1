#!/usr/bin/python3
""" Method that ensures that the tracking number is Unique """

from tracking_information.models import Tracking_info
from tracking_information.utils.track_gen import tracking_number_gen

def uniquefy(num: str, vendor: str) -> str:
    ''' Checks to see if the tracking doesn't exists in the database '''
    while Tracking_info.objects.filter(parcel_number=num).exists():
        num = tracking_number_gen(user=vendor)
    return num.upper()
