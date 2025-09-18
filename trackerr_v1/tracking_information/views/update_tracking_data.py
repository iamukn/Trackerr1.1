from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from business.views.business_owner_permission import IsBusinessOwner
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer
from shared.celery_tasks.tracking_info_tasks.verify_address_task import verify_shipping_address as validate
from django.db import transaction

class UpdateTracking(APIView):
    permission_classes = [IsBusinessOwner,]

    def get_queryset(self, num):
        obj = get_object_or_404(klass=Tracking_info, parcel_number=num.upper())
        return obj
    

    def patch(self, request, num, *args, **kwargs):
        print(num, request.user)
        obj = self.get_queryset(num=num)
        
        if obj.owner == request.user:
            # get the data and update it
            data = request.data
            old_addr = data.get('shipping_address')
            address = data.pop('shipping_address').lower()
            if not address == obj.shipping_address.lower():
                # get the address coordinate
                # add the coordinate to destination_lat and destination_lng
                # add the full address to shipping_address
                address = validate.apply_async(kwargs={'address': address}).get()
                data['country'] = address.get('country').lower()
                data['shipping_address'] = old_addr.lower()
                data['destination_lat'] = str(address.get('latitude')).lower()
                data['destination_lng'] = str(address.get('longitude')).lower()

            # initiate an atomic transaction
            try:
                with transaction.atomic():
                    serializer = Tracking_infoSerializer(obj, data=data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        print('Validddddd')
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({'msg': 'an error occurred while updated your data'}, status=status.HTTP_500_INTERNAL_SERVAL_ERROR)
        return Response({'msg': 'you are not authorized to view this resource'}, status=status.HTTP_401_UNAUTHORIZED)
