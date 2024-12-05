#!/usr/bin/python3
""" Realtime parcel location retrieving route """

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from tracking_information.utils.fetch_parcel_location import RetrieveParcelLocation
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class RealtimeParcelTracking(APIView):
    permission_classes = [AllowAny,]
    
    # swagger 
    @swagger_auto_schema(
        operation_summary='Retrieve realtime information of a tracking number',
        operation_description='Endpoint that retrieves information for a tracking number',
        manual_parameters= [
            openapi.Parameter(
            'parcel_number',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            properties={
                'parcel_number': openapi.Schema(type=openapi.TYPE_STRING, title='tracking number', description='parcel number', minLength=1)
                },
            required=True,
            example={
                'parcel_number': 'JO223603848OE'
                }
            )
            ],
        responses={
            '200': openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'rider_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unique ID of rider'),
                        'parcel_number': openapi.Schema(type=openapi.TYPE_STRING, description='Unique tracking number'),
                        'destination': openapi.Schema(type=openapi.TYPE_STRING, description='destination address'),
                        'destination_lat': openapi.Schema(type=openapi.TYPE_STRING, description='destination latitude'),
                        'destination_lng': openapi.Schema(type=openapi.TYPE_STRING, description='destination longitude'),
                        'lng': openapi.Schema(type=openapi.TYPE_STRING, description='riders longitude'),
                        'lat': openapi.Schema(type=openapi.TYPE_STRING, description='riders latitude'),
                        'rider_address': openapi.Schema(type=openapi.TYPE_STRING, description='riders current address'),
                        },
                    example={
                        "rider_id": None,
                        "parcel_number": "JO223603848OE",
                        "destination": "Bogobiri St, Calabar Municipal, Nigeria",
                        "destination_lat": "4.95896",
                        "destination_lng": "8.32666",
                        "lng": None,
                        "lat": None,
                        "rider_address": None
                    }

                    ),
                ),
            '400': openapi.Response(
                description='Error: Bad Request',
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='A tracking number is required!')
                    },
                example={
                    'detail': 'A tracking number is required!'
                    }
                ),
            '404': openapi.Response(
                description='Error: Not Found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Tracking number not valid!')
                        },
                    example={
                        'detail': 'Tracking number not valid!'
                        }
                    )
                )
            }
        )
    # receiving tracking informations as query_params
    def get(self, request, *args, **kwargs):
        if not request.query_params or not 'parcel_number' in request.query_params:
            return Response({"detail": "A tracking number is required!"}, status=status.HTTP_400_BAD_REQUEST)       
        parcel_number = request.query_params.get('parcel_number')
        
        track = RetrieveParcelLocation().get_parcel_location(parcel_number)
        if 'parcel_number' in track:
            return Response(track, status=status.HTTP_200_OK)
        return Response(track, status=status.HTTP_404_NOT_FOUND)
