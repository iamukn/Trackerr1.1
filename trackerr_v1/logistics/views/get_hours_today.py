from logistics.utils.getHours import get_today_active_hours
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .logistics_owner_permission import IsLogisticsOwner

class GetHoursToday(APIView):

    permission_classes = [IsLogisticsOwner,]

    def get(self, request, *args, **kwargs):
        get_time = get_today_active_hours(rider=request.user.id)
        print(get_time)

        if (float(get_time) < 1.0):
            m = str(get_time).split('.')[-1]
            return Response({'msg': f'{m}m'}, status=status.HTTP_200_OK)

        return Response({'msg': f'{get_time}h'}, status=status.HTTP_200_OK)
