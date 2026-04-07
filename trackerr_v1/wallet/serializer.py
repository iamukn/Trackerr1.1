from .models import Wallet, Payment
from rest_framework.serializers import ModelSerializer

class WalletSerializer(ModelSerializer):
    class Meta:
        model=Wallet
        fields='__all__'


class PaymentSerializer(ModelSerializer):
    class Meta:
        model=Payment
        fields='__all__'
