import json
from django.db import transaction
from channels.db import database_sync_to_async
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer

from logistics.models import Logistics_partner as Rider
from logistics.serializer import Logistics_partnerSerializer as serializer

@database_sync_to_async
def update_location(rider, lat, lng):
    with transaction.atomic():
        rider = Rider.objects.select_for_update().get(user=rider)
        rider_serializer = serializer(rider, data={'lat': str(lat), 'lng': str(lng)})

        if rider_serializer.is_valid():
            print(lat, lng)
            rider_serializer.save()

class RiderLocationConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'rider_location':
            await update_location(self.scope['user'], data['lat'], data['lng'])
