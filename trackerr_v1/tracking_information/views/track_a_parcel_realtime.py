#!/usr/bin/python3
""" Realtime parcel location retrieving route """

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from channels.db import database_sync_to_async


# receiving tracking informations as query_params
# db async query method
@database_sync_to_async
def get_tracking_data(parcel_number):
    from tracking_information.models import Tracking_info
    try:
        return Tracking_info.objects.get(parcel_number=parcel_number)
    except Tracking_info.DoesNotExist:
        return None


class RealtimeTracking(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print('Connected!!!')

    async def track_parcel_loop(self):
        coords = []
        rider_uuid = None
        while True:
            if not coords:
                # fetch the latest coordinates
                parcel = await get_tracking_data(parcel_number=self.tracking_number)

                if parcel:
                    coords.append(parcel)
            # get the location of the rider
            # rider_location = get_rider_location(rider_uuid)
            parcels = coords[0]

            # return only the business owner and destination location if status is either pending, delivered or returned
            if parcels.status in ['pending', 'delivered', 'returned']:
    
                location_data = {
                    'parcel': {
                        'parcel_number': self.tracking_number,
                        'status': parcels.status,
                        },
                    'locations': {
                        'business_owner': {
                            'lat': float(parcels.business_owner_lat),
                            'lng': float(parcels.business_owner_lng)
                            },
                        'customer': {
                            'lat': float(parcels.destination_lat),
                            'lng': float(parcels.destination_lng)
                            }
                        }
                        }
                await self.send(text_data=json.dumps({'location_data': location_data}))
                break
                
            
            location_data = {
                'parcel': {
                    'parcel_number': self.tracking_number,
                    'status': parcels.status,
                    },
                'locations': {
                    'business_owner': {
                        'lat': float(parcels.business_owner_lat),
                        'lng': float(parcels.business_owner_lng)
                        },
                    'customer': {
                        'lat': float(parcels.destination_lat),
                        'lng': float(parcels.destination_lng),
                        },
                    'rider': {
                        'lat': '',
                        'lng': '',
                        }
                    }
                    }
            await self.send(text_data=json.dumps({"location_data": location_data}))
            await asyncio.sleep(2)
            
    async def disconnect(self, close_code):
        print('Disconnected!!!')
        if hasattr(self, 'tracking_task'):
            self.tracking_task.cancel()
        try:
            await self.tracking_task
        except asyncio.CancelledError:
            print("Tracking task cancelled cleanly.")

    async def receive(self, text_data):
        # get the tracking number
        data = json.loads(text_data)
        self.tracking_number = data["parcel_number"]
        self.tracking_task = asyncio.create_task(self.track_parcel_loop())    
