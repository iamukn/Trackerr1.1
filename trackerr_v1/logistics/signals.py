#!/usr/bin/python3

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from logistics.models import Logistics_partner
from shared.celery_tasks.utils_tasks.send_reg_email import send_reg_email
from django.conf import settings
from shared.logger import setUp_logger

logger = setUp_logger(__name__, 'logistics.logs')
"""
    Signals to send emails as soon as a User is Created
"""

logistics_partner_created = Signal()

@receiver(logistics_partner_created)
def send_welcome_email(sender, instance, password, **kwarg):
    user = instance.user
    to = [user.email]
    username = user.name
    account_type = user.account_type

    print('SendEMailL instance, to, username, account, type: ', user, to, username, account_type, password)

    try:
        send_reg_email.apply_async(
            args=[to, username, account_type, password]
        )
    except Exception as e:
        logger.error(e)

#@receiver(post_save, sender=Logistics_partner)

#def send_welcome_email(sender, instance, created, **Kwargs):

#    if created:# only send email for new users
#        to = [instance.user.email,]
#        username=instance.user.name
#        account_type = instance.user.account_type
#        password = getattr(instance.user, '_raw_password', None)
#        try:
            # send registration email
#            send_reg_email.apply_async(
#                args=[to, username, account_type, password]
#                    )
#        except Exception as e:
            # Write a logging for this incase an exception occurs
#            logger.error(e)
