from rest_framework.serializers import ModelSerializer
from affiliate.models import Affiliate, AccountDetails

class AffiliateSerializer(ModelSerializer):

    class Meta:
        model = Affiliate
        fields = "__all__"

class AccountDetailsSerializer(ModelSerializer):

    class Meta:
        model = AccountDetails
        fields = "__all__"
