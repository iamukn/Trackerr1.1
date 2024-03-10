#!/usr/bin/python3
from django.shortcuts import get_object_or_404, Http404
from random import randint
from tracking_information.models import Tracking_info
from .track_gen import tracking_number_gen
from .track_gen_validate import uniquefy
from typing import List
""" Handles the tracking generation and manipulation """

class Track_gen:
    '''
       Tracking numer generation class
    '''
    def __init__(self):
        # fetch all the data in the tracking database
        self.tracking_db = Tracking_info.objects.all()
        
    def generate_tracking(self, vendor):
        ''' 
           This handles unique tracking number generation
           by calling the tracking_number_gen function that generates 
           the tracking
        '''
        vendor = vendor
        # Generates the tracking number
        parcel_number = tracking_number_gen(vendor).upper()
        # Verify if the tracking number is unique
        unique_num = uniquefy(num=parcel_number, vendor=vendor)
        return unique_num

    def get_tracking_info(self, num:str) -> List or Dict:
        '''
            gets the tracking information for a unique tracking number and
            returns to the calling function
            Args:
                num: The unique tracking to be lookedup
            Return: Tracking object
        '''
        num = get_object_or_404(self.tracking_db, parcel_number=num)
        return num
