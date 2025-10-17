from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from business.views.business_owner_permission import IsBusinessOwner
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer
from logistics.models import Logistics_partner
from logistics.serializer import Logistics_partnerSerializer
from shared.celery_tasks.tracking_info_tasks.verify_address_task import verify_shipping_address as validate
from shared.celery_tasks.utils_tasks.send_tracking_email import send_tracking_updates_email as send_tracking_updates
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
            address = data.pop('shipping_address') if 'shipping_address' in data else ""
            
            if address and old_addr:
                if not address.lower() == obj.shipping_address.lower():
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
                    #if 'rider_uuid' in data:
                    #    rider = get_object_or_404(Logistics_partner, logistics_owner_uuid=data.get('rider_uuid'))
                    #    rider_serializer = Logistics_partnerSerializer(rider, data={ "total_assigned_orders" : int(rider.total_assigned_orders + 1)})
                    if serializer.is_valid():
                        if 'rider_uuid' in data:
                            rider = get_object_or_404(Logistics_partner, logistics_owner_uuid=data.get('rider_uuid'))
                            rider_serializer = Logistics_partnerSerializer(rider, data={ "total_assigned_orders" : int(rider.total_assigned_orders + 1)}, partial=True)
                            if rider_serializer.is_valid():
                                rider_serializer.save()

                        if data.get('status').lower() == 'delivered':
                            auth_user = request.user.account_type
                            if auth_user.lower() == 'logistics':
                                rider = request.user
                                rider_serializer = Logistics_partnerSerializer(rider, data={ "total_delivery" : int(rider.total_delivery + 1)}, partial=True)
                                if rider_serializer.is_valid():
                                    rider_serializer.save()
                        serializer.save()
                        if data.get('status').lower() in ['assigned', 'delivered', 'returned', 'cancelled', 'canceled' ]:
                            t_data = serializer.data
                            if data.get('status').lower() == 'assigned':

                                send_tracking_updates.apply_async(
                                        kwargs={
                                            'email': t_data.get('customer_email'),
                                            'customer_name': 'There',
                                            'parcel_number': t_data.get('parcel_number'),
                                            'vendor': t_data.get('vendor'),
                                            'status': t_data.get('status'),
                                            'rider_name': t_data.get('rider_name', 'John Doe'),
                                            'rider_phone': t_data.get('rider_phone', '07044525266'),
                                             }
                                          )

                            elif data.get('status').lower() == 'delivered':
                                send_tracking_updates.apply_async(
                                        kwargs={
                                            'email': t_data.get('customer_email'),
                                            'customer_name': 'There',
                                            'parcel_number': t_data.get('parcel_number'),
                                            'status': t_data.get('status'),
                                            'vendor': t_data.get('vendor'),
                                            }
                                        )

                            elif data.get('status').lower() == 'returned':
                                send_tracking_updates.apply_async(
                                         kwargs={
                                             'email': t_data.get('customer_email'),
                                             'customer_name': 'There',
                                             'parcel_number': t_data.get('parcel_number'),
                                             'status': t_data.get('status'),
                                             'vendor': t_data.get('vendor'),
                                             }
                                         )
                            elif data.get('status').lower() in ['canceled','cancelled']:
                                send_tracking_updates.apply_async(
                                        kwargs={
                                            'email': t_data.get('customer_email'),
                                            'customer_name': 'There',
                                            'parcel_number': t_data.get('parcel_number'),
                                            'status': t_data.get('status'),
                                            'vendor': t_data.get('vendor'),
                                            }
                                        )
                            else:
                                print('Status is not one of the required statuses')
                                ...
                        
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    print(serializer.errors)
                    return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({'msg': 'an error occurred while updated your data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'you are not authorized to view this resource'}, status=status.HTTP_401_UNAUTHORIZED)
