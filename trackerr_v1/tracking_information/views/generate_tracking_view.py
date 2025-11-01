#!/usr/bin/python3
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tracking_information.utils.tracking_class import Track_gen
from tracking_information.serializer import Tracking_infoSerializer
from tracking_information.models import Tracking_info
from shared.celery_tasks.tracking_info_tasks.verify_address_task import verify_shipping_address
from shared.celery_tasks.utils_tasks.send_tracking_email import send_tracking_updates_email as send_tracking_updates
from rest_framework.permissions import IsAuthenticated 
from business.views.business_owner_permission import IsBusinessOwner
from shared.logger import setUp_logger

# logger
logger = setUp_logger(__name__, 'tracking_information.logs')

""" Route that handles tracking number generation using POST """

class GenerateView(APIView):
    permission_classes = [IsBusinessOwner,]
    

    def __init__(self):
        
        self.Track_gen = Track_gen() 
    
    # swagger generator
    @swagger_auto_schema(
        operation_summary='Endpoint that generates a tracking number',
        operation_description='Generate a tracking number',
        tags=['trackings'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'shipping_address': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='destination address'
                    ),
                'country': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='country'
                    ),
                'product': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='product name'
                    ),
                'customer_email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='customers email'
                    ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="customers phone number"
                    )
                ,
                'quantity': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='quantity of the products'
                    ),
                'delivery_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='estimated date of arrival'
                    ),
                },
            example={
                "shipping_address": "10 johnny avenue waco texas",
                "country": "United States of America",
                "product": "shoes",
                "customer_email": "johndoe@example.com",
                "phone": "08028856692",
                "quantity": "2",
                "delivery_date": "2024-12-12"
                },
            required=["shipping_address", "country","phone", "product", "customer_email", "quantity", "delivery_date"]
            ),
        # response
        responses={
            '201': openapi.Response(
                description='Tracking successfully generated',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='unique ID of the tracking number'
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
                            description='customer email'
                            ),
                        'phone': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='phone number'
                            )
                        ,
                        'delivery_date': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='delivery date'
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
                            description='current location of parcel'
                            ),
                        'country':  openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='destination country',
                                ),
                        'product_name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='product name',
                                ),
                        'quantity': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description='quantity of item shipped'
                                ),
                        'status': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='shipping status of parcel'
                                ),
                        'vendor': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='vendors name'
                                ),
                        'rider': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='riders unique ID'
                                ),
                        },
                    example={
                        "id": 3,
                        "parcel_number": "JO149230016OE",
                        "date_of_purchase": "2024-12-02",
                        "time_of_purchase": "19:47hrs",
                        "customer_email": "ukn@gmail.com",
                        "delivery_date": "2024-12-12",
                        "shipping_address": "Bogobiri St, Calabar Municipal, Nigeria",
                        "latitude": None,
                        "longitude": None,
                        "phone": "08028856629",
                        "destination_lat": "4.95896",
                        "destination_lng": "8.32666",
                        "rider_email": None,
                        "realtime_location": None,
                        "country": "Nigeria",
                        "product_name": "shoes",
                        "quantity": 2,
                        "status": "pending",
                        "vendor": "johnny_logistics",
                        "rider": None
                        }
                      )
                    ),  
            '401': openapi.Response(
                    description='Error: Unauthorized',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'detail': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Authentication credentials were not provided'
                                )
                            },
                        example={
                            'detail': 'Aunthentication credentials were not provided'
                            }
                        )
                    ),

            },

            )
    # method that handles the POST request
    def post(self, request, *args, **kwargs):
        try:
            # retrieve the location data using celery
            address = verify_shipping_address.apply_async(kwargs={'address': request.data.get('shipping_address').capitalize()}).get()
            #parcel_number = self.Track_gen.generate_tracking(vendor=request.user.name)
            # retrieves all the data from the requuest, generate a tracking number and return to user
            data = {
                "shipping_address": address.get('address').capitalize(),
                "destination_lat": address.get('latitude'),
                "destination_lng": address.get('longitude'),
                "vendor": request.user.business_owner.business_name,
                "owner": request.user.id,
                "parcel_number": self.Track_gen.generate_tracking(vendor=request.user.name),
                "country": address.get('country').capitalize(),
                "product_name": request.data.get('product').lower(),
                "customer_email": request.data.get('customer_email').lower(),
                "quantity": request.data.get('quantity'),
                "delivery_date": request.data.get('delivery_date'),
                "business_owner_lat": request.user.business_owner.latitude,
                "business_owner_lng": request.user.business_owner.longitude,
                "customer_phone": request.data.get('phone')
                    }
            ser = Tracking_infoSerializer(data=data)
            if ser.is_valid():
                ser.save()
                data = ser.data
                data.pop('owner')
                # send confirmation email
                send_tracking_updates.apply_async(kwargs={
                    "email": request.data.get('customer_email'),
                    "customer_name": "There",
                    "parcel_number": data.get('parcel_number'),
                    "vendor": data.get('vendor'),
                    "delivery_address": data.get('shipping_address'),
                    "items": data.get('product_name'),
                    "eta": data.get('delivery_date'),
                    "status": data.get('status')
                    })
                
                return Response(data, status=status.HTTP_201_CREATED)
            logger.error(ser.errors)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise(e)
            logger.error(e)
            return Response({"error":e}, status=status.HTTP_400_BAD_REQUEST)
