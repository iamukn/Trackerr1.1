#!/usr/bin/python3

from django.db.models.signals import post_save
from django.dispatch import receiver
from affiliate.models import Affiliate
from shared.celery_tasks.utils_tasks.send_reg_email import send_reg_email

"""
    Signals to send emails as soon as an Affiliate User is Created
"""

@receiver(post_save, sender=Affiliate)
def send_welcome_email(sender, instance, created, **kwarg):
    user = instance
    to = [user.email]
    username = str(user.full_name).split(' ')[0].strip()
    account_type = "affiliate"

    try:
        send_reg_email.apply_async(
            args=[to, username, account_type, ""]
        )
    except Exception as e:
        logger.error(e)
