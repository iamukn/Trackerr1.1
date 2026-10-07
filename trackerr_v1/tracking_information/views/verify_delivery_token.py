from rest_framework.views import APIView
from rest_framework import status
from logistics.views.logistics_owner_permission import IsLogisticsOwner
from rest_framework.response import Response
from tracking_information.models import Tracking_info as Model


class VerifyDeliveryToken(APIView):

    permission_classes = [IsLogisticsOwner, ]


    def post(self, request, *args, **kwargs):

        data = request.data

        parcel_number = data.get('parcel_number')
        code = data.get('otp')

        if not parcel_number and not code:
            return Response({'msg': 'error', 'details': 'parcel number and otp are required'},status=status.HTTP_400_BAD_REQUEST)
        elif not code:
            return Response({'msg': 'error', 'details': 'otp is required'},status=status.HTTP_400_BAD_REQUEST)

        if parcel_number:
            is_found = Model.objects.filter(parcel_number=parcel_number.upper())

            if is_found:
                is_valid = int(is_found[0].delivery_otp) == int(code)
                
                return Response({'msg': 'success', 'is_verified': is_valid}, status=status.HTTP_200_OK)
            return Response({'msg': 'error', 'details': 'parcel number does not exist'},status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'error', 'details': 'parcel number is required'},status=status.HTTP_400_BAD_REQUEST)
