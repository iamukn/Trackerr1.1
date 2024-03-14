#!/usr/bin/python3
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tracking_information.utils.tracking_class import Track_gen
from tracking_information.serializer import Tracking_infoSerializer
from tracking_information.models import Tracking_info
from rest_framework.permissions import IsAuthenticated 
from .business_owner_permission import IsBusinessOwner

""" Route that handles tracking number generation using POST """

class GenerateView(APIView):
    permission_classes = [IsBusinessOwner,]

    def __init__(self):
        
        self.Track_gen = Track_gen() 
    
    # method that handles the POST request

    def get(self, request, *args, **kwargs):
        
        print(request.user.business_owner.business_name)
        tracking = Tracking_info.objects.all()
        ser = Tracking_infoSerializer(tracking, many=True)

        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        try:
            data = {
                "shipping_address": request.data.get('shipping_address'),
                "vendor": request.user.business_owner.business_name,
                "owner": request.user.id,
                "parcel_number": self.Track_gen.generate_tracking(vendor=request.user.name)
                    }
            ser = Tracking_infoSerializer(data=data)
        except Exception:
            raise ValueError("An Error occured while creating the Tracking number")

        if ser.is_valid():
            ser.save()
            data = ser.data
            data.pop('owner')
            return Response(data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
       
