from rest_framework.serializers import ModelSerializer
from .models import (Logistics_partner, Business_owner)

""" 
    Serializer for handling both Logistics and Business owners model

"""

class Logistics_partnerSerializer(ModelSerializer):
    class Meta:
        model = Logistics_partner
        fields = '__all__'
        depth = 1

class Business_ownerSerializer(ModelSerializer):
    class Meta:
        model = Business_owner
        fields = '__all__'
        depth = 1
