#!/usr/bin/python3
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from tracking_information.utils.get_tracking_history_using_email import retrieve_history


""" Retrieve all tracking information shipped to a unique customer """

class Customer_history(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, *args, **kwargs):
        email = request.data.get('email')
        customer_history = retrieve_history(email)
        return Response(customer_history, status=status.HTTP_200_OK)
