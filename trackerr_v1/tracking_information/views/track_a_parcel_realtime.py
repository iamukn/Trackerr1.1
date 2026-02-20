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



    async def disconnect(self, close_code):
        print("WebSocket disconnected")
        # Remove from group if assigned
        if hasattr(self, 'rider_group_name'):
            await self.channel_layer.group_discard(
                self.rider_group_name, self.channel_name
            )            


    async def receive(self, text_data):
        """
        Receive tracking number from client and join the rider's group.
        """
        data = json.loads(text_data)
        self.tracking_number = data.get("parcel_number").upper()

        # Fetch parcel info once
        parcel = await get_tracking_data(self.tracking_number)
        if not parcel:
            await self.send(json.dumps({"error": "Parcel not found"}))
            await self.close()
            return

        # Store required fields for reuse during broadcasts
        self.parcel_status = parcel.status
        self.country = parcel.country.lower()
        self.customer_lat = float(parcel.destination_lat)
        self.customer_lng = float(parcel.destination_lng)

        # Create a group per rider (broadcast updates to this group)
        self.rider_group_name = f"rider_{parcel.rider_uuid}"
        print('Rider_Group_Joined:', parcel.rider_uuid)
        await self.channel_layer.group_add(
            self.rider_group_name, self.channel_name
        )

        # Send initial parcel info (status + business_owner & customer)
        location_data = {
            "parcel": {
                "parcel_number": self.tracking_number,
                "status": parcel.status,
            },
            "locations": {
                "business_owner": {
                    "lat": float(parcel.business_owner_lat),
                    "lng": float(parcel.business_owner_lng)
                },
                "customer": {
                    "lat": float(parcel.destination_lat),
                    "lng": float(parcel.destination_lng)
                }
            }
        }
        await self.send(text_data=json.dumps({"location_data": location_data}))

    async def rider_location_update(self, event):
        """
        Called when the rider endpoint broadcasts a new location.
        """
        lat = event["lat"]
        lng = event["lng"]

        location_data = {
            'parcel': {
                'parcel_number': self.tracking_number,
                },
            'locations': {
                'rider': {
                    'lat': float(lat),
                    'lng': float(lng),
                }
            }
        }

        location_data = {
            "parcel": {
                "parcel_number": self.tracking_number,
                "status": self.parcel_status,
            },
            "country": self.country,
            "locations": {
                "customer": {
                    "lat": self.customer_lat,
                    "lng": self.customer_lng,
                },
                "rider": {
                    "lat": float(lat),
                    "lng": float(lng),
                }
            }
        }

        # Send the updated rider location to the client
        await self.send(text_data=json.dumps({
            'location_data': location_data
            }
        ))
