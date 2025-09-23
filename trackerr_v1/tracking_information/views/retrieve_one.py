#!/usr/bin/python3
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer


""" Retrieves tracking information for a tracking number """

class RetrieveOne(APIView):
    # retrieves data for a tracking number

    permission_classes = [AllowAny,]

    def query_set(self, num:str):
        track = get_object_or_404(Tracking_info, parcel_number=num.upper())
        return track
    # Swagger documentation
    @swagger_auto_schema(
        operation_description='Retrieve tracking information for a tracking number',
        operation_summary='Get information about a tracking number',
        responses={
            '200': openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_NUMBER, description='unique ID of the tracking'),
                        'parcel_number': openapi.Schema(type=openapi.TYPE_STRING, description='tracking number'),
                        'date_of_purchase': openapi.Schema(type=openapi.TYPE_STRING, description='date of purchase'),
                        'time_of_purchase': openapi.Schema(type=openapi.TYPE_STRING, description='time of purchase'),
                        'customer_email': openapi.Schema(type=openapi.TYPE_STRING, description='customers email'),
                        'delivery_date': openapi.Schema(type=openapi.TYPE_STRING, description='delivery date'),
                        'shipping_address':openapi.Schema(type=openapi.TYPE_STRING, description='shipping address'),
                        'latitude': openapi.Schema(type=openapi.TYPE_STRING, description='riders latitude or null'),
                        'longitude': openapi.Schema(type=openapi.TYPE_STRING, description='riders longitude or null'),
                        'destination_lat': openapi.Schema(type=openapi.TYPE_STRING, description='destination latitude'),
                        'destination_lng': openapi.Schema(type=openapi.TYPE_STRING, description='destination longitude'),
                        'rider_email': openapi.Schema(type=openapi.TYPE_STRING, description='riders email'),
                        'realtime_location': openapi.Schema(type=openapi.TYPE_STRING, description='location of parcel of null'),
                        'country': openapi.Schema(type=openapi.TYPE_STRING, description='destination country'),
                        'product_name': openapi.Schema(type=openapi.TYPE_STRING, description='product name'),
                        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='quantity of product'),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='delivery status of parcel'),
                        'vendor': openapi.Schema(type=openapi.TYPE_STRING, description='vendors name'),
                        'rider': openapi.Schema(type=openapi.TYPE_STRING, description='rider unique ID'),
                        }
                    ),
                ),
            '404': openapi.Response(
                description='Error: Not Found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='No Tracking_info matches the given query.')
                        },
                    example={
                        'detail': "No Tracking_info matches the given query."
                        }
                    ),
                ),
            },
            )
    def get(self, request, num:str, *args, **kwargs):
        """ handles retrieving tracking information for a unique tracking number """
        data = self.query_set(num)
        # checks if a data was returned from the database
        # if yes, it serializes it and send to the user
        serializer = Tracking_infoSerializer(data)
        data = serializer.data
        data.pop('owner')
        data['shipping_address'] = data.get('shipping_address').title()
        data['country'] = data.get('country').title()
        return Response(data, status=status.HTTP_200_OK)
