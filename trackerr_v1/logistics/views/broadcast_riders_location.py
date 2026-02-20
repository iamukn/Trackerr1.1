#!/usr/bin/python3
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class BroadcastLocation(APIView):
    ''' receives the riders latitude and longitude for broadcast to connected clients '''
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        # gets the rider uuid and the cordinates sent from the rider app
        rider_uuid = request.user.logistics_partner.logistics_owner_uuid
        lat = request.data['lat']
        lng = request.data['lng']

        channel_layer = get_channel_layer()

        # Broadcast to relevant WebSocket groups
        async_to_sync(channel_layer.group_send)(
            f"rider_{rider_uuid}",
            {
                "type": "rider_location_update",
                "lat": lat,
                "lng": lng
            }
        )
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
