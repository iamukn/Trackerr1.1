from .models import Wallet
from rest_framework.serializers import ModelSerializer

class WalletSerializer(ModelSerializer):
    class Meta:
        model=Wallet
        fields='__all__'
