from rest_framework.serializers import ModelSerializer
from .models import Logistics_partner

"""
  Serializer for handling Logistics model
"""

class Logistics_partnerSerializer(ModelSerializer):
    """
      Seializer for the Logistics Partner
    """

    class Meta:
        model = Logistics_partner
        fields = '__all__'
        depth = 1
