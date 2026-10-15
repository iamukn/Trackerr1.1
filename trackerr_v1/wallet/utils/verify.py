from wallet.models import Payment

def validate_idempotency_key(idempotency_key):

    payment = Payment.objects.filter(idempotency_key=idempotency_key).first()

    if payment and payment.status == 'pending':
        return payment.authorization_url
    return False
