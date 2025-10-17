#!/usr/bin/python3

from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Otp
from django.conf import settings
from shared.logger import setUp_logger
from wallet.models import Wallet
from decimal import Decimal

logger = setUp_logger(__name__, 'user.logs')
"""
    Signals to create Otp linked to a user
"""

@receiver(post_save, sender=User)
def create_otp_model_for_user(sender, instance, created, **Kwargs):

    if created:# create otp for a user
        user = instance
        try:
            # create the otp model
            otp = Otp(
                owner=user
                    )
            otp.save()
            logger.info('Otp created and assigned to {}'.format(otp.owner.name))

            # create the wallet for users
            country = user.country

            if country.lower()  == 'ghana':
                wallet = Wallet(
                        owner = user,
                        balance = Decimal(f'{500 * 0.05}'),
                        currency = 'GHC'
                        )
            elif country.lower()  == 'nigeria':
                wallet = Wallet(
                        owner = user,
                        balance = Decimal('500.00'),
                        currency = 'NGN'
                        )
            wallet.save()
            logger.info('Wallet created and assigned to {} with balance {} {}'.format(wallet.owner.name, wallet.balance, wallet.currency))
            print('Wallet created and assigned to {} with balance {} {}'.format(wallet.owner.name, wallet.balance, wallet.currency))
        except Exception as e:
            # Write a logging for this incase an exception occurs
            logger.error(e)
