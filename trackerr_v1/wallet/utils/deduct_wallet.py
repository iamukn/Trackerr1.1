from wallet.models import Wallet
from django.core.exceptions import ValidationError
from django.core.cache import cache
from decimal import Decimal

def deduct_wallet(user):
    wallet = user.wallet
    country = user.country
    if country.lower() == 'nigeria':
        # deduct 150 naira from Nigerian accounts
        amount = 150
    elif country.lower() == 'ghana':
        # deduct 4 cedis from Ghanian accounts
        amount = Decimal('1.2')

    balance = wallet.balance

    if balance < amount:
        raise ValidationError('Insuffient balance, please top up!❌')
        return


    wallet.balance -= amount
    if wallet.balance <=0:
        wallet.balance = 0
    wallet.save()
    cache.delete(f'business_owner_{user.business_owner.id}_data')

    return wallet.balance
