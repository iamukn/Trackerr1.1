from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_list_or_404
from business.views.business_owner_permission import IsBusinessOwner
from logistics.models import Logistics_partner
from logistics.serializer import Logistics_partnerSerializer
from user.models import User
from django.core.cache import cache


class Business_Riders(APIView):
    permissions_classes = [IsBusinessOwner, ]

    def get_queryset(self, model, owner):
        return get_list_or_404(model, owner=owner)

    def get(self, request, *args, **kwargs):
        
        # get all riders
        try:
            vendor = request.user.business_owner
            if cache.has_key(f'business_owner_riders:{vendor.business_owner_uuid}'):
                print('Gotten from cache')
                return Response({'msg': cache.get(f'business_owner_riders:{vendor.business_owner_uuid}')}, status=status.HTTP_200_OK)
            riders = self.get_queryset(model=Logistics_partner, owner=vendor.id)
            riders_serializer = Logistics_partnerSerializer(riders, many=True)
            cache.set(f'business_owner_riders:{vendor.business_owner_uuid}', riders_serializer.data, timeout=6000)
            print('Not from cache')
            return Response({'msg': riders_serializer.data}, status=status.HTTP_200_OK)
        except User.business_owner.RelatedObjectDoesNotExist:
            return Response({'msg': {'you are not authorized to view this resource'}}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            raise(e)
            return Response({'msg': {'internal server error'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
