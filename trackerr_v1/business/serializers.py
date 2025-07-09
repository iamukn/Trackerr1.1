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
        #fields = '__all__'
        exclude = ['business_owner_uuid', 'profile_pic_key']

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'business_name' in data:
            data['business_name'] = data['business_name'].lower()
        return data

    def update(self, instance, validated_data):
        # Optional: fallback to raw request data (if fields are excluded from serializer)
        request = self.context.get('request').data
        if request:
           if 'profile_pic_key' in request:
                instance.profile_pic_key = request.get('profile_pic_key')
           if 'business_owner_uuid' in request:
                instance.business_owner_uuid = request.get('business_owner_uuid')

        instance.save()
        return instance
