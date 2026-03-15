from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer
from logistics.views.logistics_owner_permission import IsLogisticsOwner
from django.core.cache import cache

class GetDeliveries(APIView):
    permission_classes = [IsLogisticsOwner,]


    def get(self, request, *args, **kwargs):
        rider = request.user.logistics_partner
        if cache.has_key(f'all_deliveries_{rider.id}'):
            return Response( cache.get(f'all_deliveries_{rider.id}'), status=status.HTTP_200_OK)
        data = Tracking_info.objects.filter(rider=rider)
        serializer = Tracking_infoSerializer(data, many=True)
        # add to cache
        cache.set(f'all_deliveries_{rider.id}', serializer.data, timeout=30)
        return Response(serializer.data, status=status.HTTP_200_OK)
