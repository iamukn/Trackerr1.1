#!/usr/bin/python3
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from logistics.models import Logistics_partner
from logistics.serializer import Logistics_partnerSerializer
from .logistics_owner_permission import IsLogisticsOwner

""" Update Riders Location """

class UpdateLocation(APIView):
    """ Handles updating the logistics owners location """

    permission_classes = [IsLogisticsOwner,]
    
    # Swagger documentation
    @swagger_auto_schema(
        tags=['Logistics Partner']
            )
    def patch(self, request, *args, **kwargs):
        
        data = request.data
        lat = data.get('lat')
        lng = data.get('lng')
        # get the users model
        #user = get_object_or_404(Logistics_partner, user=request.user.id)
        # serializes the data
        try:
            with transaction.atomic():
                user = Logistics_partner.objects.select_for_update().get(user=request.user.id)
                serializer = Logistics_partnerSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    # saves the model with the new data
                    serializer.save()
                    # removes the users data from the object
                    data = serializer.data
                    data.pop('user')
                    # returns a 206
                    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
                # returns a 400 if the incorrect fields are passed
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Logistics_partner.DoesNotExist:
            return Response({'msg': 'rider does not exist'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'msg': 'an error occurred'}, status=HTTP_400_BAD_REQUEST)
