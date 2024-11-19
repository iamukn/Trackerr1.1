from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from .models import (User, Otp)

""" 
    Serializer for the User model

"""

class UsersSerializer(ModelSerializer):
    logo = SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'


    def get_logo(self, obj):
        if obj.logo:  # If logo field is not empty
            return obj.logo.url  # Assuming logo is a FileField or ImageField
        else:
            return None

    def to_internal_value(self, validated_data):
        # convert fields to lowercase for consistency
        validated_data = super().to_internal_value(validated_data)
        if validated_data.get('name'):
            validated_data['name'] = validated_data['name'].lower()
        if validated_data.get('email'):
            validated_data['email'] = validated_data['email'].lower()
        if validated_data.get('address'):
            validated_data['address'] = validated_data['address'].lower()
        return validated_data

    def to_representation(self, instance):
        instance = {
            "name": instance.name,
            "email": instance.email,
            "phone_number": instance.phone_number,
            "is_verified": instance.is_active, 
            "account_type": instance.account_type,
            "address": instance.address
                }
        return instance

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'account_type' in validated_data:
            validated_data.pop('account_type')
        return super().update(instance, validated_data)
