from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer
from logistics.views.logistics_owner_permission import IsLogisticsOwner

class GetDeliveries(APIView):
    permission_classes = [IsLogisticsOwner,]


    def get(self, request, *args, **kwargs):
        data = Tracking_info.objects.filter(rider=request.user.logistics_partner)

        serializer = Tracking_infoSerializer(data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
