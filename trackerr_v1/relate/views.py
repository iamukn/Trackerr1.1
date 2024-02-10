from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Tracking
from .serializer import TrackingSerializer

class Home(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        queryset = Tracking.objects.all()
        ser = TrackingSerializer(queryset, many=True)

        return Response(ser.data, status=200)

