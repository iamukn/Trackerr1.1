from rest_framework import serializers
from .models import Logistics_partner, LogisticsOwnerStatusLog
from user.serializers import UsersSerializer
from logistics.signals import logistics_partner_created

"""
  Serializer for handling Logistics model
"""

class Logistics_partnerSerializer(serializers.ModelSerializer):
    """
      Seializer for the Logistics Partner
    """
    user = UsersSerializer(required=False, read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Logistics_partner
        exclude = ['vehicle_image_key']



    def create(self, validated_data):
        raw_password = validated_data.pop('password', None)

        print(raw_password)

        logistics_partner = Logistics_partner.objects.create(
            **validated_data
        )

        # Emit your custom signal here
        logistics_partner_created.send(
            sender=Logistics_partner,
            instance=logistics_partner,
            password=raw_password
        )

        return logistics_partner



class LogisticsOwnerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsOwnerStatusLog
        fields = "__all__"
        read_only_fields = ["timestamp"]
