from rest_framework.serializers import ModelSerializer
from .models import Business_owner
from user.models import User
from user.serializers import UsersSerializer

"""
  Serializer for handling Business owners model
"""


class Business_ownerSerializer(ModelSerializer):
    """
      Business Owners Serializer
    """

    class Meta:
        model = Business_owner
        fields = '__all__'
        depth = 1
