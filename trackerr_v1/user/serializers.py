from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (User, Logistics_partner, Business_owner)

""" 
    Serializer for handling both Logistics and Business owners model

"""

class UsersSerializer(ModelSerializer):
    logo = SerializerMethodField()
    class Meta:
        model = User
        exclude = ['password']

    def get_logo(self, obj):
        if obj.logo:  # If logo field is not empty
            return obj.logo.url  # Assuming logo is a FileField or ImageField
        else:
            return None

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
