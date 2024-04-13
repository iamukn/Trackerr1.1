#!/usr/bin/env python3
""" class that fetches the location of a parcel """
from django.core.exceptions import ObjectDoesNotExist
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer
from typing import Dict

class RetrieveParcelLocation(object):

    def __init__(self):
        """ initializes the tracking_update class"""

        self.tracking_num = Tracking_info.objects.all()

    def get_parcel_location(self, track_num:str) -> Dict:
        try:
            track_num = self.tracking_num.get(parcel_number = track_num)
            track_num_ser = Tracking_infoSerializer(track_num)
            # check if the tracking number is valid
            
            location = {
                "carrier_id" : track_num_ser.data.get('carrier_id'),
                "parcel_number" : track_num_ser.data.get('parcel_number'),
                "destination" : track_num_ser.data.get('shipping_address'), # this location will be gotten from the logistic owners profile which woll constantly be updating
                "destination_lat" : track_num_ser.data.get('destination_lat'),
                "destination_lon" : track_num_ser.data.get('destination_lon'),
                "lon" : track_num_ser.data.get('longitude'),
                "lat" : track_num_ser.data.get('latitude'),
                "address" : track_num_ser.data.get('realtime_location')

                    }
            # return a list of the parcel location
            return location

        except ObjectDoesNotExist:
            response = {'detail' : 'Tracking number not valid!'}
            return response
