from rest_framework.serializers import ModelSerializer
from .models import Phone

class PhoneSerializer(ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'
