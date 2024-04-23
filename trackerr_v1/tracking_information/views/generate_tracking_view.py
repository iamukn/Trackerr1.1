#!/usr/bin/python3
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tracking_information.utils.tracking_class import Track_gen
from tracking_information.serializer import Tracking_infoSerializer
from tracking_information.models import Tracking_info
from tracking_information.utils.validate_shipping_address import verify_address
from rest_framework.permissions import IsAuthenticated 
from business.views.business_owner_permission import IsBusinessOwner

""" Route that handles tracking number generation using POST """

class GenerateView(APIView):
    permission_classes = [IsBusinessOwner,]
    

    def __init__(self):
        
        self.Track_gen = Track_gen() 
    
    # method that handles the POST request
    def post(self, request, *args, **kwargs):
        try:

            address = verify_address(request.data.get('shipping_address'))
            # retrieves all the data from the requuest, generate a tracking number and return to user
            data = {
                "shipping_address": address.get('address'),
                "destination_lat": address.get('latitude'),
                "destination_lng": address.get('longitude'),
                "vendor": request.user.business_owner.business_name,
                "owner": request.user.id,
                "parcel_number": self.Track_gen.generate_tracking(vendor=request.user.name),
                "country": address.get('country'),
                "product_name": request.data.get('product'),
                "quantity": request.data.get('quantity'),
                "delivery_date": request.data.get('delivery_date'),
                    }
            ser = Tracking_infoSerializer(data=data)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_400_BAD_REQUEST)
            #raise ValueError("An Error occured while creating the Tracking number")

        if ser.is_valid():
            ser.save()
            data = ser.data
            data.pop('owner')
            return Response(data, status=status.HTTP_201_CREATED)
        
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)       
