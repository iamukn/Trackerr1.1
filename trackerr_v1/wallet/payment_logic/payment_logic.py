import os
import requests
from decimal import Decimal, InvalidOperation

PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
PAYSTACK_INIT_URL = os.environ.get('PAYSTACK_INIT_URL')


def initialize_payment(email, amount, currency='NGN') -> dict:
    try:
        amount = float(Decimal(amount) * 100)

        payload = {
            'email' : email,
            'amount' : amount,
            'currency' : 'NGN'
                }

        headers = {
                'Authorization' : 'Bearer {}'.format(PAYSTACK_SECRET_KEY),
                'Content-Type' : 'application/json'
                }

        response = requests.post(PAYSTACK_INIT_URL, headers=headers, json=payload)
        return response.json()
    except InvalidOperation as e:
        raise ValueError('invalid amount')
