#!/usr/bin/python3
""" Realtime parcel location retrieving route """

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from tracking_information.utils.fetch_parcel_location import RetrieveParcelLocation


class RealtimeParcelTracking(APIView):
    permission_classes = [AllowAny,]
    
    """ receiving tracking informations as query_params """
    def get(self, request, *args, **kwargs):
        if not request.data:
            return Response({"detail": "A tracking number is required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        parcel_number = request.query_params.get('parcel_number')
        
        track = RetrieveParcelLocation().get_parcel_location(parcel_number)
        if 'parcel_number' in track:
            return Response(track, status=status.HTTP_200_OK)
        return Response(track, status=status.HTTP_404_NOT_FOUND)
