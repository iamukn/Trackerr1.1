from logistics.utils.getHours import get_today_active_hours
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .logistics_owner_permission import IsLogisticsOwner

# cache
from django.core.cache import cache

class GetHoursToday(APIView):

    permission_classes = [IsLogisticsOwner,]

    def get(self, request, *args, **kwargs):
        rider = request.user

        if cache.has_key(f'hours_today:{rider.id}'):
            data = cache.get(f'hours_today:{rider.id}')
            return Response({'msg': f'{data}'}, status=status.HTTP_200_OK)
        get_time = get_today_active_hours(rider=rider.id)
        # set cache
        cache.set(f'hours_today:{rider.id}', get_time, timeout=500)
        return Response({'msg': f'{get_time}'}, status=status.HTTP_200_OK)
