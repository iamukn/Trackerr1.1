from django.urls import path
from wallet.routes.payment import PaymentWebhook

urlpatterns = [
    path('webhook', PaymentWebhook.as_view(), name='payment-webhook')
        ]
