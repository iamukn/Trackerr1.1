from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from .models import (User, Otp)
from django.utils.timezone import now


""" 
    Serializer for the User model

"""

class UsersSerializer(ModelSerializer):
    logo = SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'


    def get_logo(self, obj):
        if obj.avatar:  # If logo field is not empty
            return obj.avatar.url  # Assuming logo is a FileField or ImageField
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
        if validated_data.get('avatar'):
            validated_data['avatar'] = validated_data['avatar']
        return validated_data

    def to_representation(self, instance):

        user_instance = {
            "id": instance.id,
            "name": instance.name,
            "email": instance.email,
            "phone_number": instance.phone_number,
            "is_verified": instance.is_active, 
            "account_type": instance.account_type,
            "address": instance.address,
            "is_verified": instance.is_verified,
            "is_active": instance.is_active,
            "created_on": instance.date_joined,
            "updated_on": instance.updated_on
                }
        
        if instance.avatar:
            # get the avatar url
            avatar_url = instance.avatar.url
            # get the request object
            request = self.context.get('request')
            if request:
                # build an absolute url
                avatar_url = request.build_absolute_uri(avatar_url)
                user_instance['avatar'] = avatar_url
        else:
            user_instance['avatar'] = ""
        return user_instance

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'account_type' in validated_data:
            validated_data.pop('account_type')
        for attr, val in validated_data.items():
            if attr == "avatar" and val:
                # delete the previous avatar
                instance.avatar.delete()
            setattr(instance, attr, val)
        setattr(instance, "updated_on", now())
        instance.save()
        return instance
