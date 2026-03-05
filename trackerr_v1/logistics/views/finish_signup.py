from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from logistics.serializer import LogisticsOwnerStatusSerializer, Logistics_partnerSerializer
from .logistics_owner_permission import IsLogisticsOwner
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny
from user.serializers import UsersSerializer
from user.models import User
from django.db import transaction

from os import environ
from shared.celery_tasks.business_owners_task.upload_dp import upload_dp


class CompleteSignup(APIView):
    permission_classes=[IsLogisticsOwner,]
    parser_classes=(MultiPartParser, FormParser, JSONParser)

    def patch(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                user = User.objects.select_for_update().get(id=request.user.id)
                rider = user.logistics_partner

                # Get the image
                avatar = request.data.get('avatar')
                # prepare the data and upload image to rider s3
                CDN_URL = environ.get('TRACKERR_CDN_URL')
                # upload the avatar to S3
                upload_dp.delay(file_obj=avatar.read(), key=str(avatar))

                data_params = {"plate_number" : data.get('number_plate') ,
                        "terms_and_condition" : bool(data.get('terms_and_condition')),
                        "vehicle_color" : data.get('vehicle_color'),
                        "vehicle_model": data.get("vehicle_model"),
                        "profile_pic_key" : str(avatar)
                        }

                rider_serializer = Logistics_partnerSerializer(rider, data=data_params, partial=True)
                
                print(f'{CDN_URL}/{str(avatar)}')
                user_serializer = UsersSerializer(user, data={'is_verified': True,
                    'avatar': f'{CDN_URL}/{str(avatar)}'}, partial=True)

                if rider_serializer.is_valid() and user_serializer.is_valid():
                    user_serializer.save()
                    rider_serializer.save()
                    return Response({"msg": "success"}, status=status.HTTP_200_OK)
                return Response({'msg': "error"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise(e)
            return Response({'msg': "error", "details": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
