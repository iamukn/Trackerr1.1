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

    # convert from kobo to naira or to cedis
    amount = amount / 100

    # deduct the vat  from the amount
    amount = Decimal(amount) - Decimal(vat)
    return amount
