#!/usr/bin/env python3
""" class that fetches the location of a parcel """

from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer

# dummy location data for tracking parcel location
riders_location = ['Ikeja', 'Umuahia', 'Uyo', 'FCT', 'Ilorin', 'Jalingo', 'Jos']

class Tracking_update(object):

    def __init__(self):
        """ initializes the tracking_update class"""

        self.tracking_num = Tracking_info.objects.all()

    def update_tracking_info(self, num:str) -> dict:
        pass
