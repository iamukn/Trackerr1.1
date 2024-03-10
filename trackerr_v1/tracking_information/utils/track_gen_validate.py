#!/usr/bin/python3
""" Method that ensures that the tracking number is Unique """

from tracking_information.models import Tracking_info
from tracking_information.utils.track_gen import tracking_number_gen

def uniquefy(num: str, vendor: str) -> str:
    ''' Checks to see if the tracking doesn't exists in the database '''
    if not Tracking_info.objects.filter(parcel_number=num).exists():
        
        return num.upper()
    # If the tracking exist in  the database, a recursive call is made
    num = tracking_number_gen(user=vendor)
    uniquefy(num=num, vendor=vendor)
