#!/usr/bin/env python3
""" view that handles activity charts"""

from django.contrib.auth.models import AnonymousUser as Anon
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from tracking_information.utils.get_days_or_month_tracking_count import ActivityChart
from business.views.business_owner_permission import IsBusinessOwner

class GetWeeklyActivityChart(APIView):
    """ returns the activity charts for the last 7 days """
    
    permission_classes = [IsBusinessOwner,]
    chart = ActivityChart()

    def get(self, request, *args, **kwargs):
        # check if it's an anonymousUser
        if isinstance(request.user,Anon):
            return Response({'details': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            return Response(self.chart.last_seven_days(request.user), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

class GetMonthlyActivityChart(GetWeeklyActivityChart):
    """ returns the activity charts for the last one month """

    def get(self, request, *args, **kwargs):
        # check if it's an anonymousUser
        if isinstance(request.user,Anon):
            return Response({'details': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            return Response(self.chart.last_month_count(request.user), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
