from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from decimal import Decimal
import uuid
"""
    The Logistic parner model that inherits from
    the User model
"""

class Logistics_partner(models.Model):
    """ 
        Model that relatates the User to Logistics partner
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lat = models.CharField(max_length=55, null=True, blank=True)
    lng = models.CharField(max_length=55, null=True, blank=True)
    identity_card_type = models.CharField(max_length=120, null=True, blank=True)
    id_number = models.CharField(max_length=50, null=True, blank=True, unique=True)
    plate_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    owner = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    vehicle_model = models.CharField(max_length=50, null=True, blank=True)
    logistics_owner_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile_pic_key = models.CharField(max_length=300, null=True, blank=True)
    vehicle_color = models.CharField(max_length=50, null=True, blank=True)
    vehicle_image_key = models.CharField(max_length=300, null=True, blank=True)
    referral_code = models.CharField(max_length=50, null=True, blank=True)
    terms_and_condition = models.BooleanField(null=True, blank=True)
    is_busy = models.BooleanField(null=False, blank=False, default=False)
    total_delivery = models.IntegerField(blank=False, null=False, default=0)
    total_assigned_orders = models.IntegerField(blank=False, null=False, default=0)
    rating = models.FloatField(blank=False, null=False, default=float(0))
    status = models.CharField(max_length=50, null=False, blank=False, default='inactive')


    # add rider uuid here
    def __str__(self):
        """
          String representation of the logistics partner
        """
        return "Rider: {} {}".format(self.user.name, self.identity_card_type)


class LogisticsOwnerStatusLog(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)   # "active" or "inactive"
    timestamp = models.DateTimeField(auto_now_add=True)
