from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Arr
from .serializer import ArrSerializer

class arrView(APIView):
    permission = [AllowAny]


    def get(self, request, *args, **kwargs):

        data = Arr.objects.all()
        ser = ArrSerializer(data, many=True)
        return Response(ser.data, status='200')
