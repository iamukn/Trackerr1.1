from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from business.views.business_owner_permission import IsBusinessOwner
from logistics.serializer import Logistics_partnerSerializer
from logistics.models import Logistics_partner
from .logistics_owner_permission import IsLogisticsOwner
from user.serializers import UsersSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import Http404
from shared.celery_tasks.business_owners_task.upload_dp import upload_dp
from shared.celery_tasks.utils_tasks.delete_existing_file import delete_old_file
from os import environ


class Rider(APIView):
    permissions_classes = (IsLogisticsOwner, IsBusinessOwner)
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_queryset(self, model: object, pk:int ):
        rider = get_object_or_404(model, id=pk)

        return rider

    def get(self, request, id,  *args, **kwargs):

        rider = self.get_queryset(model=Logistics_partner, pk=id)

        if request.user.account_type == 'logistics' and not id == request.user.logistics_partner.id:
            return Response({'msg': 'you are not unauthorized to vuew this resource'}, status=status.HTTP_401_UNAUTHORIZED)

        elif request.user.account_type == 'business' and not rider.owner == request.user.business_owner.id:
            return Response({'msg': 'you are not unauthorized to view this resource'}, status=status.HTTP_401_UNAUTHORIZED)

        rider_serializer = Logistics_partnerSerializer(rider)

        data = rider_serializer.data
        data['user']['avatar'] = f"{environ.get('TRACKERR_CDN_URL')}/{data.get('profile_pic_key')}"

        return Response({'msg': rider_serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id,  *args, **kwargs):
        # retrieve rider model
        try:
            rider = self.get_queryset(model=Logistics_partner, pk=id)

            if rider:
                user = rider.user

            if request.user.account_type == 'logistics' and not id == request.user.logistics_partner.id:
                return Response({'msg': 'you are not unauthorized to update this resource'}, status=status.HTTP_401_UNAUTHORIZED)

            elif request.user.account_type == 'business' and not rider.owner == request.user.business_owner.id:
                return Response({'msg': 'you are not unauthorized to update this resource'}, status=status.HTTP_401_UNAUTHORIZED)

            if not rider:
                return Response({'msg': 'rider does not exist'}, status=status.HTTP_404_NOT_FOUND)

            data = request.data.copy()

            if 'avatar' in data:
                avatar = data.pop('avatar')
                # update the avatar using the profile pic key

                avatar = avatar[0]
                content_type = avatar.content_type.split('/')[-1]
                if not content_type.lower() in ['jpg', 'jpeg', 'png']:
                    return Response({'msg': 'avatar must be in jpg, png or jpeg format'}, status=status.HTTP_400_BAD_REQUEST)
                
                old_profile_pic_key = rider.profile_pic_key
                profile_pic_key = f'{old_profile_pic_key.split(".")[0]}.{content_type}'
                data['profile_pic_key'] = profile_pic_key
                
                # delete old file from server if the extension differs
                if not old_profile_pic_key == profile_pic_key:
                    delete_old_file.delay(oldKey=old_profile_pic_key)

                # upload the new avatar
                upload_dp.delay(avatar.read(), profile_pic_key)


            for key in data.copy().keys():

                if key in ['vehicle_model', 'vehicle_color',
                                    'vehicle_image','password', 
                                    'terms_and_condition', 'nationality',
                                    'plate_number', 'id_number', 
                                    'identity_card_type', 'email', 'account_type'
                                    ]:
                    print('Popped: ', key)
                    data.pop(key)
            rider_serializer = Logistics_partnerSerializer(rider, data=data, partial=True)
            user_serializer = UsersSerializer(user, data=data, partial=True)

            with transaction.atomic():
                if rider_serializer.is_valid() and user_serializer.is_valid():
                    rider_serializer.save()
                    user_serializer.save()
                    return Response({'msg': 'rider updated successfully'}, status=status.HTTP_200_OK)

                elif not rider_serializer.is_valid():
                    # log errors to logger
                    return Response({'msg': rider_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                elif not user_serializer.is_valid():
                    # log errors to logger
                    return Response({'msg': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request, id,  *args, **kwargs):
        # delete a rider model
        try:
            rider = self.get_queryset(model=Logistics_partner, pk=id)

            if rider:
                user = rider.user

            if request.user.account_type == 'logistics' and not id == request.user.logistics_partner.id:
                return Response({'msg': 'you are not unauthorized to delete this user'}, status=status.HTTP_401_UNAUTHORIZED)

            elif request.user.account_type == 'business' and not rider.owner == request.user.business_owner.id:
                return Response({'msg': 'you are not unauthorized to delete this user'}, status=status.HTTP_401_UNAUTHORIZED)


            rider = rider.user.delete()
            return Response({'msg': f'rider: {user.name} deleted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'msg': 'rider not found!'}, status=status.HTTP_404_NOT_FOUND)
