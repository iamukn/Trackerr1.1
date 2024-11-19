from rest_framework.serializers import ModelSerializer
from .models import Logistics_partner
from user.serializers import UsersSerializer

"""
  Serializer for handling Logistics model
"""

class Logistics_partnerSerializer(ModelSerializer):
    """
      Seializer for the Logistics Partner
    """
    user = UsersSerializer(required=False, read_only=True)

    class Meta:
        model = Logistics_partner
        fields = '__all__'
