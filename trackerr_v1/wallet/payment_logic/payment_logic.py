import os
import requests
from wallet.utils.calc_vat import calc_vat
from decimal import Decimal, InvalidOperation

# Nigeria paystack secret key
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
# Ghana Paystack secret key
PAYSTACK_SECRET_KEY_GH = os.environ.get('PAYSTACK_SECRET_KEY_GH')
PAYSTACK_INIT_URL = os.environ.get('PAYSTACK_INIT_URL')


def initialize_payment(email, amount, country, currency='NGN') -> dict:
    try:

        amount = float(Decimal(amount) * 100)
        vat = calc_vat(amount=amount, country=country)

        payload = {
            'email' : email,
            'amount' : int(amount + float(vat)),
            'currency' : currency
                }

        if currency == 'GHS':

            headers = {
                'Authorization' : 'Bearer {}'.format(PAYSTACK_SECRET_KEY_GH),
                'Content-Type' : 'application/json'
                    }
        else:
            headers = {
                'Authorization' : 'Bearer {}'.format(PAYSTACK_SECRET_KEY),
                'Content-Type' : 'application/json'
                }

        response = requests.post(PAYSTACK_INIT_URL, headers=headers, json=payload)
        data = response.json()
        data['vat'] = vat
        return data
    except InvalidOperation as e:
        raise ValueError('invalid amount')
