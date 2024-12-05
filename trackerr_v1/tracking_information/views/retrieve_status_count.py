#!/usr/bin/python3
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from business.views.business_owner_permission import IsBusinessOwner
from tracking_information.utils.fetch_tracking_status_count import tracking_status_count as status_count


""" 
    Route that handles the tracking data counts on the business owner dashboard
    Returns the total tracking generated, and counts based on the tracking status
"""

class RetrieveStatusCount(APIView):

    permission_classes = [IsBusinessOwner,]
    
    # Swagger Generator
    @swagger_auto_schema(
        operation_summary='Retrieve Tracking Number Status Counts',
        operation_description='Endpoint the retrieves the counts of the tracking number status',
        responses = {
            '200': openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "delivered_status_count": openapi.Schema(type=openapi.TYPE_NUMBER, description='delivered parcel status count'),
                        "returned_status_count": openapi.Schema(type=openapi.TYPE_NUMBER, description='returned parcel status count'),
                        "pending_status_count": openapi.Schema(type=openapi.TYPE_NUMBER, description='pending parcel status count'),
                        "total_tracking_generated": openapi.Schema(type=openapi.TYPE_NUMBER, description='total tracking generated'),
                        },
                    example={
                        "delivered_status_count": 0,
                        "returned_status_count": 0,
                        "pending_status_count": 4,
                        "total_tracking_generated": 4
                        }
                    )
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authorization credentials were not provided.')
                        },
                    example={
                        'detail': 'Authorization credentials were not provided.'
                        }
                    )
                )
            }
            )
    def get(self, request, *args, **kwargs):
        # fetches the tracking number counts for a unique user
        data = status_count(request.user)

        if not len(data) < 2:
            return Response(data, status=status.HTTP_200_OK)

        return Response(data, status=status.HTTP_404_NOT_FOUND)
