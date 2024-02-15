from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (User,)

""" 
    Serializer for the User model

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
