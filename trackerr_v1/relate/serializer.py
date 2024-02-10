from rest_framework.serializers import ModelSerializer
from .models import Tracking

class TrackingSerializer(ModelSerializer):
    class Meta:
        model = Tracking
        fields = '__all__'
        depth = 1


