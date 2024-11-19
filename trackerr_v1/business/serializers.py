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
    user = UsersSerializer(required=False, read_only=True)

    class Meta:
        model = Business_owner
        fields = '__all__'

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'business_name' in data:
            data['business_name'] = data['business_name'].lower()
        return data
