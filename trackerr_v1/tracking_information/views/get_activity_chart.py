#!/usr/bin/env python3
""" view that handles activity charts"""

from django.contrib.auth.models import AnonymousUser as Anon
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from tracking_information.utils.get_days_or_month_tracking_count import ActivityChart
from business.views.business_owner_permission import IsBusinessOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GetWeeklyActivityChart(APIView):
    """ returns the activity charts for the last 7 days """
    
    permission_classes = [IsBusinessOwner,]
    chart = ActivityChart()
    # swagger documentation
    @swagger_auto_schema(
        operation_summary='GET weekly activity chart',
        operation_description='GET: Retrieve weekly activity chart',
        responses={
            '200': openapi.Response(
                description='Weekly chart',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "Mon": openapi.Schema(type=openapi.TYPE_INTEGER, description='total tracking generated on Monday'),
                        "Tue": openapi.Schema(type=openapi.TYPE_INTEGER, description='total tracking generated on Tuesday'),
                        "Wed": openapi.Schema(type=openapi.TYPE_INTEGER, description='total tracking generated on Wednesday'),
                        "Thur": openapi.Schema(type=openapi.TYPE_INTEGER, description='total tracking generated on Thursday'),
                        "Fri": openapi.Schema(type=openapi.TYPE_INTEGER, description='total tracking generated on Friday'),
                        "Sat": openapi.Schema(type=openapi.TYPE_INTEGER, description='total tracking generated on Saturday'),
                        "Sun": openapi.Schema(type=openapi.TYPE_INTEGER, description='total tracking generated on Sunday'),
                        },
                    example={
                        "Mon": 2,
                        "Tue": 2,
                        "Wed": 0,
                        "Thur": 0,
                        "Fri": 0,
                        "Sat": 0,
                        "Sun": 0
                        }
                    )
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided.')
                        }
                    )
                )
            }
            )
    def get(self, request, *args, **kwargs):
        # check if it's an anonymousUser
        if isinstance(request.user,Anon):
            return Response({'details': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            last_seven = self.chart.last_seven_days(request.user)
            return Response(last_seven, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

class GetMonthlyActivityChart(GetWeeklyActivityChart):
    """ returns the activity charts for the last one month """
    # swagger 
    @swagger_auto_schema(
        operation_description='Retrieve Monthly Activity Chart',
        operation_summary='GET monthly summary',
        responses = {
            '200': openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'Week One': openapi.Schema(type=openapi.TYPE_INTEGER, description='number of tracking generated in the first week'),
                        'Week Two': openapi.Schema(type=openapi.TYPE_INTEGER, description='number of tracking generated in the second week'),
                        'Week Three': openapi.Schema(type=openapi.TYPE_INTEGER, description='number of tracking generated in the third week'),
                        'Week Four': openapi.Schema(type=openapi.TYPE_INTEGER, description='number of tracking generated in the fourth week'),
                        },
                    example={
                        'Week One': 1,
                        'Week Two': 12,
                        'Week Three': 29,
                        'Week Four': 0
                        }
                    )
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided.')
                        },
                    example={
                        'detail': 'Authentication credentials were not provided.'
                        }
                    )
                )
            }
            )
    def get(self, request, *args, **kwargs):
        # check if it's an anonymousUser
        if isinstance(request.user,Anon):
            return Response({'details': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            return Response(self.chart.last_month_count(request.user), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
