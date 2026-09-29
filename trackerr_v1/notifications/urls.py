from django.urls import path
from notifications.routes.webhook import WhatsappWebhook

urlpatterns = [
    path('whatsapp/webhook', WhatsappWebhook.as_view(), name="whatsapp-webhook") 
        ]
