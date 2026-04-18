from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from logistics.serializer import Logistics_partnerSerializer
from logistics.permissions.logistics_owner_permissions import IsRider

class UpdatePushNotificationToken(APIView):

    permission_classes = [IsRider,]

    def post(self, request, *args, **kwargs):

        try:
            token = request.data.get('expo_push_token')

            if not token:
                return Response({'error': 'expo push token is required!'}, status=status.HTTP_400_BAD_REQUEST)
            
            rider = request.user.logistics_partner

            data = {
                'expo_notif_token': token
                    }
            
            serializer = Logistics_partnerSerializer(rider, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
