#!/usr/bin/python3
from celery import shared_task
from django.utils import timezone


def set_rider_offline(rider_instance):
    rider_instance.status = 'inactive'
    rider_instance.save()

def handle_rider_state():
    from logistics.models import Logistics_partner as Riders
    active_riders =  Riders.objects.filter(status='active')

    for rider in active_riders:
        updated_on = rider.updated_on
        now = timezone.now()

        time_diff = now - updated_on
        time_diff = int(time_diff.total_seconds())
        
        if time_diff > 120:
            # uncomment the set_rider call below so that the heartbeat can function
            #set_rider_offline(rider)
            ...

@shared_task(bind=True, name='rider_online_offline')
def handle_rider_status(self,):
    handle_rider_state()
