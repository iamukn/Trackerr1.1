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
        while True:
            # fetch the latest coordinates
            parcel = await get_tracking_data(parcel_number=self.tracking_number)
            coords = {"lat": parcel.latitude, "long": parcel.longitude}

            await self.send(text_data=json.dumps({"location": coords}))
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
