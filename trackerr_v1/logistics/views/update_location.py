import json
from django.db import transaction
from channels.db import database_sync_to_async
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer

from logistics.models import Logistics_partner as Rider
from logistics.serializer import Logistics_partnerSerializer as serializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@database_sync_to_async
def update_location(rider, lat, lng):
    with transaction.atomic():
        rider = Rider.objects.select_for_update().get(user=rider)
        rider_serializer = serializer(rider, data={'lat': str(lat), 'lng': str(lng)})
        
        if rider_serializer.is_valid():
            rider.save()
            return rider_serializer.data.get('logistics_owner_uuid')

class RiderLocationConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data['lat'], data['lng'])

        if data['type'] == 'rider_location':
            rider_uuid = await update_location(self.scope['user'], data['lat'], data['lng'])

            # broadcast
            await self.channel_layer.group_send(
                 f"rider_{rider_uuid}",
                 {
                    "type": "rider_location_update",
                    "lat": data['lat'],
                    "lng": data['lng']
                 }
            )
