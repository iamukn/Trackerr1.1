"""
   Converts the raw Naira amount to the actual amount equivalent in
   the clients local currency
"""
from decimal import Decimal
from wallet.models import Payment

def actual_amount_paid(amount, vat, country):
    # convert vat from naira to kobo
    vat = vat / 100
    if country not in ['ghana', 'nigeria']:
        return 0

    # convert from kobo to naira
    amount = amount / 100

    # deduct the vat  from the amount
    amount = Decimal(amount) - Decimal(vat)

    # convert to ghana currency
    if country == 'ghana':
        # 4/9/2026 1 GHS = 123.3 NGN 
        rate = 123.3
        amount = amount / Decimal(rate)

    return amount
