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
        #exclude = ['business_owner_uuid']

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'business_name' in data:
            data['business_name'] = data['business_name'].lower()
        return data

    def update(self, instance, validated_data):

        for key in ['profile_pic_key', 'business_owner_uuid', 'business_name', 'service', 'latitude', 'longitude']:
            if key in validated_data:
                setattr(instance, key, validated_data[key])
            else:
                request_data = self.context.get('request').data
                if key in request_data:
                    setattr(instance, key, request_data.get(key))
        instance.save()
        return instance
