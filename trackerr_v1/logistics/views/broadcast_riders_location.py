#!/usr/bin/python3
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from logistics.permissions.logistics_owner_permissions import IsRider
from django.core.cache import cache


class BroadcastLocation(APIView):
    ''' receives the riders latitude and longitude for broadcast to connected clients '''
    permission_classes = [IsRider,]

    def post(self, request, *args, **kwargs):
        # gets the rider uuid and the cordinates sent from the rider app
        rider_uuid = request.user.logistics_partner.logistics_owner_uuid
    
        old_lat = cache.get(f'rider_{request.user.id}_lat')
        old_lng = cache.get(f'rider_{request.user.id}_lng')
        # new lat
        lat = request.data.get('lat')
        lng = request.data.get('lng')

        if lat == old_lat and lng == old_lng:
            return Response({"status": "ok"}, status=status.HTTP_200_OK)

        #set the lat n lng to cache
        cache.set(f'rider_{request.user.id}_lat', lat)
        cache.set(f'rider_{request.user.id}_lng', lng)

        channel_layer = get_channel_layer()

        if not lat or not lng:
            print('No lat or lng')

        # Broadcast to relevant WebSocket groups
        broadcast = {
            "type": "rider_location_update",
            "lat": lat,
            "lng": lng
                }
        async_to_sync(channel_layer.group_send)(
            f"rider_{rider_uuid}",
            broadcast
        )
        print(f'location broadcasted as: {broadcast}')
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
