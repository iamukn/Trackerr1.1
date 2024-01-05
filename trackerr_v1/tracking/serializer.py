from .models import Tracking
from rest_framework.serializers import ModelSerializer



class TrackingSerializer(ModelSerializer):
    class Meta:
        model = Tracking
        fields = '__all__'

        depth = 1
