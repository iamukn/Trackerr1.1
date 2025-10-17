from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from logistics.serializer import  Logistics_partnerSerializer
from user.serializers import UsersSerializer
from user.models import User
from django.db import transaction
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from shared.celery_tasks.business_owners_task.upload_dp import upload_dp
from logistics.utils.generate_password import generate_password
import uuid


class RegisterRider(APIView):
    permission_classes = [AllowAny, ]
    parser_classes = (MultiPartParser,  FormParser, JSONParser,)

    def post(self, request,  *args, **kwargs):

        data = request.data.copy()
        rider_uuid = uuid.uuid4()


        if 'password' in data:
            data.pop('password')

        avatar = ""
        vehicle_image = "" 

        if 'avatar' in data:
            avatar =  data.pop('avatar')[0]
            file_extension = avatar.content_type.split('/')[-1]
            profile_pic_key = f'riders_dp/{rider_uuid}.{file_extension}'
            data['profile_pic_key'] = profile_pic_key

 #       if not 'vehicle_image' in data:
 #           return Response({'msg': 'vehicle image is required'}, status=status.HTTP_400_BAD_REQUEST)

        if 'vehicle_image' in data:
            vehicle_image = data.pop('vehicle_image')[0]
            file_extension = vehicle_image.content_type.split('/')[-1]
            if not file_extension.lower() in ['jpeg', 'jgp', 'png']:
                return Response({'msg': 'vehicle image must be either jpeg, png or jpg'}, status=status.HTTP_400_BAD_REQUEST)

            vehicle_image_key = f'vehicle_image/{rider_uuid}.{file_extension}'
            data['vehicle_image_key'] = vehicle_image_key




        if not 'account_type' in data:
            return Response({'msg': {'account type is required'}}, status=status.HTTP_400_BAD_REQUEST)

        # create an automic query
        if isinstance(request.user, AnonymousUser):
            return Response({'msg':'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            with transaction.atomic():

                password = generate_password()

                data['password'] = password

                new_user =  UsersSerializer(data=data)

                if request.user.account_type == 'business':
                    data['owner'] = int(request.user.business_owner.id)
                new_rider = Logistics_partnerSerializer(data=data)

                if new_user.is_valid() and new_rider.is_valid():
                    if avatar:
                        # upload avatar
                        upload_dp.delay(avatar.read(), profile_pic_key)
                    if vehicle_image:
                        # upload vehicle image
                        upload_dp.delay(vehicle_image.read(), vehicle_image_key)

                    new_user.save()
                    new_rider.save(user=get_object_or_404(User, pk=new_user.instance.id))

                    print(new_rider.instance.profile_pic_key)
                    
                    return Response({'msg': 'rider added successfully!'}, status=status.HTTP_201_CREATED)
                elif not new_user.is_valid():
                    error = new_user.errors
                    return Response({'msg': error}, status=status.HTTP_400_BAD_REQUEST)
                elif not new_rider.is_valid():
                    error = new_rider.errors
                    return Response({'msg': error}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
