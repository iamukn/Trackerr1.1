from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from rest_framework import status
import os
# Create your views here.


class WhatsappWebhook (APIView):

    permission_classes = [AllowAny,]

    def post(self, request):

        data = request.data

        return HttpResponse(status.HTTP_200_OK)

    def get(self, request):

        data = request.query_params

        if request.method == "GET":
            mode = data.get("hub.mode")
            token = data.get("hub.verify_token")
            challenge = data.get("hub_challenge")

        if mode == "subscribe" and token == os.environ.get('VERIFY_TOKEN'):
            return HttpResponse(challenge, status.HTTP_200_OK)

        return HttpResponse("Forbidden", status.HTTP_403_FORBIDDEN)
