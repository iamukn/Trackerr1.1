#!/usr/bin/python3
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .logistics_owner_permission import IsLogisticsOwner
from tracking_information.models import Tracking_info 
from tracking_information.serializer import Tracking_infoSerializer
from tracking_information.utils.get_tracking_history_using_email import retrieve_history


""" Retrieve all tracking information shipped to a unique customer """

class Rider_history(APIView):
    permission_classes = [IsLogisticsOwner,]
    
    # Swagger Documentation
    @swagger_auto_schema(
        operation_summary='Retrieve all tracking for a user',
        operation_description='GET all tracking assigned to a rider using the rider model',
        tags=['trackings'],
        manual_parameters=[
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                description='email for fetching tracking data history',
                type=openapi.TYPE_STRING,
                required=True
                )
            ],
        responses={
            '200': openapi.Response(
                description='Data Retrieved Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='tracking number unique ID'),
                            'parcel_number': openapi.Schema(type=openapi.TYPE_STRING, description='tracking number'),
                            'date_of_purchase': openapi.Schema(type=openapi.TYPE_STRING, description='date of purchase'),
                            'time_of_purchase': openapi.Schema(type=openapi.TYPE_STRING, description='time of purchase'),
                            'customer_email': openapi.Schema(type=openapi.TYPE_STRING, description='email address'),
                            'delivery_date': openapi.Schema(type=openapi.TYPE_STRING, description='delivery date'),
                            'shipping_address': openapi.Schema(type=openapi.TYPE_STRING, description='shipping address'),
                            'latitude': openapi.Schema(type=openapi.TYPE_STRING, description='origin latitude or null'),
                            'longitude': openapi.Schema(type=openapi.TYPE_STRING, description='origin longitude or null'),
                            'destination_lat': openapi.Schema(type=openapi.TYPE_STRING, description='destination latitude'),
                            'destination_lng': openapi.Schema(type=openapi.TYPE_STRING, description='destination longitude'),
                            'rider_email': openapi.Schema(type=openapi.TYPE_STRING, description='email of assigned rider'),
                            'realtime_location': openapi.Schema(type=openapi.TYPE_STRING, description='parcel location or null'),
                            'country': openapi.Schema(type=openapi.TYPE_STRING, description='destination country'),
                            'product_name':openapi.Schema(type=openapi.TYPE_STRING, description='product name'),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='quantity of products'),
                            'status': openapi.Schema(type=openapi.TYPE_STRING, description='delivery status of the tracking number'),
                            'vendor': openapi.Schema(type=openapi.TYPE_STRING, description='vendors name'),
                            'rider': openapi.Schema(type=openapi.TYPE_STRING, description='assigned rider unique ID or null'),
                            'owner': openapi.Schema(type=openapi.TYPE_STRING, description='owners unique ID'),
                            'details': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'status1': openapi.Schema(type=openapi.TYPE_STRING, description='status of tracking'),
                                        'status2': openapi.Schema(type=openapi.TYPE_STRING, description='eta status of tracking'),
                                        }
                                    )
                                )
                            },
                        ),
                        example=[
                            {
                                "id": 2,
                                "parcel_number": "JO223603848OE",
                                "date_of_purchase": "2024/12/02",
                                "time_of_purchase": "19:42hrs",
                                "customer_email": "johndoe@gmail.com",
                                "delivery_date": "2024-12-12",
                                "shipping_address": "Bogobiri St, Calabar Municipal, Nigeria",
                                "latitude": None,
                                "longitude": None,
                                "destination_lat": "4.95896",
                                "destination_lng": "8.32666",
                                "rider_email": None,
                                "realtime_location": None,
                                "country": "Nigeria",
                                "product_name": "shoes",
                                "quantity": 2,
                                "status": "pending",
                                "vendor": "johnny_logistics",
                                "rider": None,
                                "owner": 77,
                                "details": {
                                    "status1": "JO223603848OE is pending",
                                    "status2": "Estimated time of arrival~ pending"
                                    }
                            },
                                ]
                    ),
                ),
            '400': openapi.Response(
                    description='Error: Bad Request',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'detail': openapi.Schema(type=openapi.TYPE_STRING, description='enter a valid email address!')
                            },
                        example={
                            'detail': 'enter a valid email address!'
                                },
                        )
                    )
            }
            )
    # Retrieve all tracking for a user
    def get(self, request, *args, **kwargs):
        trackings = Tracking_info.objects.filter(rider=request.user.logistics_partner)
        print(trackings)
        trackings_serializer = Tracking_infoSerializer(trackings, many=True)
        return Response(trackings_serializer.data, status=status.HTTP_200_OK)
