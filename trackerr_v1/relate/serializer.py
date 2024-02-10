from rest_framework.serializers import ModelSerializer
from .models import Tracking

class TrackingSerializer(ModelSerializer):
    class Meta:
        model = Tracking
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['user']['password'], data['user']['email']
        return data

