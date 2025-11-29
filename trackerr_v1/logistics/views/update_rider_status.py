from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from logistics.serializer import LogisticsOwnerStatusSerializer
from .logistics_owner_permission import IsLogisticsOwner

class RiderStatus(APIView):

    # set rider status

    def post(self, request, *args, **kwargs):
        user =  request.user
        data = request.data.get('status')


        serializer = LogisticsOwnerStatusSerializer(data={'status': data, 'rider': user.id})

        if serializer.is_valid():
            serializer.save()
            print('Created', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
