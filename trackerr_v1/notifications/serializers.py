from rest_framework.serializers import ModelSerializer
from notifications.models import WhatsappNotification

class WhatsappNotificationSerializer(ModelSerializer):

    class Meta:
        model = WhatsappNotification
        fields = '__all__'
