#!/usr/bin/python3
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from tracking_information.models import Tracking_info
from tracking_information.serializer import Tracking_infoSerializer
from business.views.business_owner_permission import IsBusinessOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

""" Route that handles retrieving the tracking information generated by a business owner"""

class RetrieveAllView(APIView):
    permission_classes = [IsBusinessOwner,]

    def __init__(self):
        
        self.all_tracking = Tracking_info.objects.all()

    class CustomPaginator(PageNumberPagination):
        page_size = 3  # Number of items per page
        page_size_query_param = 'page_size'  # Allow client to set page size
        max_page_size = 100  # Maximum allowed page size
    
    @swagger_auto_schema(
        operation_summary='GET all trackings',
        operation_description='Endpoint that retrieves all tracking numbers and its information',
        tags=['trackings'],
        responses={
            '200': openapi.Response(
                description='Retrieves all tracking information data', 
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(
                                type=openapi.TYPE_NUMBER,
                                description='unique identifier of the tracking number'
                                ),
                            'parcel_number': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='tracking number'
                                ),
                            'date_of_purchase': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='date of purchase'
                                ),
                            'time_of_purchase': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='time of purchase'
                                ),
                            'customer_email': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='customers email'
                                ),
                            'delivery_date': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='delivery_date'
                                ),
                            'shipping_address': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='shipping address'
                                ),
                            'latitude': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='origin latitude or null'
                                ),
                            'longitude': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='origin longitude or null'
                                ),
                            'destination_lat': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='destination latitude'
                                ),
                            'destination_lng': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='destination longitude'
                                ),
                            'rider_email': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='riders email or null'
                                ),
                            'realtime_location': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='realtime location of parcel or null'
                                    ),
                            'country': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='destination country'
                                    ),
                            'product_name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='product name'
                                    ),
                            'quantity': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='quantity of items'
                                    ),
                            'status': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='shipping status'
                                    ),
                            'vendor': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='business owners name'
                                    ),
                            'rider': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='riders unique ID or null'
                                ),
                            'owner': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='tracking numbers owner unique ID'
                                ),
                            },
                        example=[
                            {
                            "id": 2,
                            "parcel_number": "JO223603848OE",
                            "date_of_purchase": "2024-12-02",
                            "time_of_purchase": "19:42hrs",
                            "customer_email": "ukn@gmail.com",
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
                            "owner": 77
                            },
                            ]
                        )
                    )
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Given token not valid for any token type',
                            ),
                        'code': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='token_not_valid'
                            ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'token_class': openapi.Schema(type=openapi.TYPE_STRING, description='AccessToken'),
                                    'token_type': openapi.Schema(type=openapi.TYPE_STRING, description='access'),
                                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Token is invalid or expired'),
                                    }
                                ),
                            )
                        },
                    example={
                        "detail": "Given token not valid for any token type",
                        "code": "token_not_valid",
                        "messages": [
                            {
                                "token_class": "AccessToken",
                                "token_type": "access",
                                "message": "Token is invalid or expired"
                            }
                                    ]
                        },
                    )
                    )
            }
            )
    # method that handles returning all tracking number generated by a user
    def get(self, request, *args, **kwargs):
        try:
            all_tracking = self.all_tracking.filter(owner=request.user.id).order_by('-id')
                    # Apply pagination
            paginator = self.CustomPaginator()
            paginated_queryset = paginator.paginate_queryset(all_tracking, request)
            serializer = Tracking_infoSerializer(paginated_queryset, many=True)
                    # Return paginated response
            return paginator.get_paginated_response(serializer.data)
            #return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            raise ValueError(
                    "An Error occured while fetching all the \
                    Tracking number generated by %s"% request.user.name \
                    )
