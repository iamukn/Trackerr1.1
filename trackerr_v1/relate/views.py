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

    def post(self, request):
        serializer = TrackingSerializer(data=request.data)
        serializer.user = request.user
        if serializer.is_valid():
            serializer.save()
            return Response('200:OKKK')
        return Response('Error Occured')
