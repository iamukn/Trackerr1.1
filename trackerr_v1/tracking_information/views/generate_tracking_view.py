#!/usr/bin/python3
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tracking_information.utils.tracking_class import Track_gen
from tracking_information.serializer import Tracking_infoSerializer
from tracking_information.models import Tracking_info
from shared.celery_tasks.tracking_info_tasks.verify_address_task import verify_shipping_address
from tracking_information.utils.validate_shipping_address import verify_address
from rest_framework.permissions import IsAuthenticated 
from business.views.business_owner_permission import IsBusinessOwner
from shared.logger import setUp_logger

# logger
logger = setUp_logger(__name__, 'tracking_information.logs')

""" Route that handles tracking number generation using POST """

class GenerateView(APIView):
    permission_classes = [IsBusinessOwner,]
    

    def __init__(self):
        
        self.Track_gen = Track_gen() 
    
    # method that handles the POST request
    def post(self, request, *args, **kwargs):
        try:
            #address = verify_address(request.data.get('shipping_address'))
            # retrieve the location data using celery
    
            address = verify_shipping_address.apply_async(kwargs={'address': request.data.get('shipping_address')}).get()
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
                "customer_email": request.data.get('customer_email'),
                "quantity": request.data.get('quantity'),
                "delivery_date": request.data.get('delivery_date'),
                    }
            ser = Tracking_infoSerializer(data=data)
        except Exception as e:
            print(e)
            logger.error(e)
            return Response({"error":e}, status=status.HTTP_400_BAD_REQUEST)
            #raise ValueError("An Error occured while creating the Tracking number")

        if ser.is_valid():
            ser.save()
            data = ser.data
            data.pop('owner')
            return Response(data, status=status.HTTP_201_CREATED)
        logger.error(ser.errors)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)       
