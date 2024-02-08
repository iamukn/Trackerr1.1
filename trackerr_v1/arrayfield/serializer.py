from .models import Arr
from rest_framework.serializers import ModelSerializer

class ArrSerializer(ModelSerializer):
    class Meta:
        model = Arr
        fields = '__all__'

