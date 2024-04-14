#!/usr/bin/python3
""" Updates Logistic owners location """

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from logistics.models import Logistics_partner
from logistics.serializer import Logistics_partnerSerializer
from .logistics_owner_permission import IsLogisticsOwner


class UpdateLocation(APIView):
    """ Handles updating the logistics owners location """

    permission_classes = [IsLogisticsOwner,]

    def post(self, request, *args, **kwargs):
        
        data = request.data
        lat = data.get('lat')
        lng = data.get('lng')
        # get the users model
        user = get_object_or_404(Logistics_partner, user=request.user.id)
        # serializes the data
        serializer = Logistics_partnerSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # saves the model with the new data
            serializer.save()
            # returns a 206
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        # returns a 400 if the incorrect fields are passed
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
