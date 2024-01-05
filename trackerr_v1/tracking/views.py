from django.shortcuts import render
from .models import Tracking
from .serializer import TrackingSerializer
from rest_framework.viewsets import ModelViewSet

class Track(ModelViewSet):
    serializer_class = TrackingSerializer


    def get_queryset(self):
        return Tracking.objects.all()


# Create your views here.
