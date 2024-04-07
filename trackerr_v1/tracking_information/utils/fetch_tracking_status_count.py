#!/usr/bin/python3

from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer
from json import dumps
from typing import Dict


""" 
  method that fetches the tracking information using the \
  tracking number and counts the status of each tracking number
"""

def tracking_status_count(user:Dict) -> Dict:
    """
    Receives a user and checks for tracking number \
    associated with that user, count the status and return
    Args:
        user: the user object from the request object
        e.g request.user
    """ 

    try:
        user = user.id
        # fk=ilters the tracking database for tracking unique to a user
        tracking_data = Tracking_info.objects.filter(owner=user)
        # fetches the total count of the data
        total_tracking = tracking_data.count()

        delivered_status_count = returned_status_count = pending_status_count = 0
        # creates the count for the delivered, returned, or pending tracking information
        for tracking_info in tracking_data:
            if tracking_info.status == 'delivered':
                delivered_status_count += 1
            elif tracking_info.status == 'returned':
                returned_status_count += 1
            else:
                pending_status_count += 1

        counts = {'delivered_status_count': delivered_status_count, \
                'returned_status_count': returned_status_count,\
                'pending_status_count': pending_status_count,\
                'total_tracking_generated': total_tracking,
                }

        # serialize and return the count to the calling function
        return counts
    except Exception as e:
        # returns the exceotion details
        return {"details": e}
