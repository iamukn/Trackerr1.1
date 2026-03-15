from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        # retrieve the users id if he's a business owner
        if hasattr(user, 'business_owner'):
            business_owner_id = user.business_owner.id
            data['id'] = business_owner_id
            data['account_type'] = user.account_type
        elif user.is_superuser and user.is_admin:
            data['id'] = user.id
            data['account_type'] = user.account_type
        elif hasattr(user, 'logistics_partner'):
            logistics_partner_id = user.logistics_partner.id
            data['id'] = logistics_partner_id
            data['account_type'] = user.account_type

        return data
