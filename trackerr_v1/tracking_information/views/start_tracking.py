from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from logistics.views.logistics_owner_permission import IsLogisticsOwner
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer
from logistics.models import Logistics_partner
from shared.celery_tasks.utils_tasks.send_tracking_email import send_tracking_updates_email as send_tracking_updates
from django.core.exceptions import ValidationError
from django.db import transaction

class StartTracking(APIView):
    permission_classes = [IsLogisticsOwner, ]

    def get_queryset(self, num):
        obj = Tracking_info.objects.select_for_update().get(parcel_number=num.upper())
        return obj


    def patch(self, request, *args, **kwargs):
        parcel_number = request.data.get('parcel_number')
        track_now = {"track_now": request.data.get('track_now')}
        
        try:
            with transaction.atomic():
                parcel = self.get_queryset(parcel_number)
                serializer = Tracking_infoSerializer(parcel, data=track_now, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    # send email
                    if track_now.get('track_now'):
                        send_tracking_updates.apply_async(
                            kwargs={
                                'email': serializer.data.get('customer_email'),
                                'customer_name': serializer.data.get('customer_name'),
                                'parcel_number': parcel_number,
                                'status': track_now.get('track_now'),
                                'vendor': serializer.data.get('vendor')
                                }
                            )
                    return Response({
                        'status': 'success',
                        'msg' : 'updated successfully'
                        }, status=status.HTTP_200_OK)
                    return Response({'status': 'error', 'msg': 'update failed, please try again'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({ 'status': 'error', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
