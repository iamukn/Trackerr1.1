#!/usr/bin/python3
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from logistics.models import Logistics_partner

""" View that returns the logistics owners count"""


class Logistics_owners_count(APIView):
    permission_classes = [IsAdminUser,]
    # Swagger documentation
    @swagger_auto_schema(
        operation_description="Retrieve the total number of logistics parners",
        operation_summary="Total number of logistics partners",
        tags=['Logistics Partner'],
        responses={
            '200': openapi.Response(
                description='Sucessful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_riders': openapi.Schema(type=openapi.TYPE_NUMBER, description='total number of logistics partners')
                        },
                    example={
                        'total_riders': 245
                        }
                    )
                ),
            '401': openapi.Response(
                description="Error: Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description="error message")
                        },
                    example={
                        'detail': 'Authentication credentials were not provided.'
                        }
                    )
                    ),
            '403': openapi.Response(
                description="Error: Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message')
                        },
                    example={
                        'detail': 'You do not have permission to perform this action.'
                        }
                    )
                )
            }
            )
    def get(self, request, *args, **kwargs):
        # Returns the count of the logistics partners 
        counts = Logistics_partner.objects.all().count()
        counts = {'total_riders': counts}

        return Response(counts, status=status.HTTP_200_OK)
