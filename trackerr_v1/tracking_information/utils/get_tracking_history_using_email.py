#!/usr/bin/env python3
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer


""" Returns tracking numbers linked to a parcular customer """

def retrieve_history(email: str) -> list:
    if not email or '@' not in email:
        return {'detail': 'Enter a valid email address!'}
    
    try:
        tracking_info = Tracking_info.objects.filter(customer_email=email)
        serializer = Tracking_infoSerializer(tracking_info, many=True)
        return serializer.data
    except Exception as e:
        return e
