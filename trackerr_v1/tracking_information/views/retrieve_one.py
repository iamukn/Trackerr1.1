#!/usr/bin/python3
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer


""" Retrieves tracking information for a tracking number """

class RetrieveOne(APIView):
    # retrieves data for a tracking number

    permission_classes = [AllowAny,]

    def query_set(self, num:str):
        track = get_object_or_404(Tracking_info, parcel_number=num)
        return track

    def get(self, request, num:str, *args, **kwargs):
        """ handles retrieving tracking information for a unique tracking number """
        data = self.query_set(num)
        # checks if a data was returned from the database
        # if yes, it serializes it and send to the user
        serializer = Tracking_infoSerializer(data)
        data = serializer.data
        data.pop('owner')
        return Response(data, status=status.HTTP_200_OK)
