from .models import Trackings
from rest_framework.serializers import ModelSerializer



class TrackingSerializer(ModelSerializer):
    class Meta:
        model = Trackings
        fields = '__all__'

        depth = 1
