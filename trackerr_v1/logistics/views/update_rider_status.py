from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from logistics.serializer import LogisticsOwnerStatusSerializer, Logistics_partnerSerializer
from .logistics_owner_permission import IsLogisticsOwner

class RiderStatus(APIView):

    # set rider status

    def post(self, request, *args, **kwargs):
        user =  request.user
        data = request.data.get('status')
        print(data)


        serializer = LogisticsOwnerStatusSerializer(data={'status': data, 'rider': user.id})
        rider_serializer = Logistics_partnerSerializer(user.logistics_partner, data={'status': data})

        if serializer.is_valid() and rider_serializer.is_valid():
            serializer.save()
            rider_serializer.save()
            print('Created', serializer.data)
            print(rider_serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
