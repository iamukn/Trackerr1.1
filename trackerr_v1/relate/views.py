from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Tracking
from .serializer import UniqueTrackingSerializer, TrackingSerializer
from django.contrib.auth.models import User

class Home(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        queryset = Tracking.objects.all()
        ser = TrackingSerializer(queryset, many=True)

        return Response(ser.data, status=200)

    def post(self, request):
        serializer = TrackingSerializer(data=request.data)
        user = User.objects.get(username=request.user)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response('200:OKKK')
        return Response('Error Occured')

class Unique(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Tracking.objects.filter(user__username=request.user)
        serializer = UniqueTrackingSerializer(queryset, many=True)

        return Response(serializer.data, status=200)
