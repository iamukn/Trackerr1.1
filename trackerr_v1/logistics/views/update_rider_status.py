from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from logistics.serializer import LogisticsOwnerStatusSerializer

class RiderStatus(APIView):

    # set rider status

    def post(self, request, *args, **kwargs):
        user =  request.user
        data = request.data.get('status')


        serializer = LogisticsOwnerStatusSerializer(data={'status': data, 'user': user.id})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
