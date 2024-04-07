#!/usr/bin/python3
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

    def get(self, request, *args, **kwargs):
        # fetches the tracking number counts for a unique user
        data = status_count(request.user)

        if not len(data) < 2:
            return Response(data, status=status.HTTP_200_OK)

        return Response(data, status=status.HTTP_404_NOT_FOUND)
