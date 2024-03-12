#!/usr/bin/python3
from .models import Tracking_info
from rest_framework.serializers import ModelSerializer
from tracking_information.models import Tracking_info

""" A serializer class for the tracking_information """

class Tracking_infoSerializer(ModelSerializer):
    
    class Meta:
        model = Tracking_info
        fields = '__all__'
