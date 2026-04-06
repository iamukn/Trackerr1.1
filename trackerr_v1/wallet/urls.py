from django.urls import path
from wallet.routes.payment import PaymentWebhook, PaymentDeposit

urlpatterns = [
    path('initialize', PaymentDeposit.as_view(), name='initialize-deposit'),
    path('webhook', PaymentWebhook.as_view(), name='payment-webhook')
        ]
