#!/usr/bin/python3

from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User, Otp
from django.conf import settings
from shared.logger import setUp_logger

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
        except Exception as e:
            # Write a logging for this incase an exception occurs
            logger.error(e)
