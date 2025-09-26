from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
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
    identity_card_type = models.CharField(max_length=120, null=False, blank=False)
    id_number = models.CharField(max_length=50, null=False, blank=False, unique=True)
    plate_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    owner = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=50, null=False, blank=False)
    vehicle_model = models.CharField(max_length=50, null=False, blank=False)
    logistics_owner_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile_pic_key = models.CharField(max_length=300, null=True, blank=True)
    vehicle_color = models.CharField(max_length=50, null=False, blank=False)
    vehicle_image_key = models.CharField(max_length=300, null=True, blank=True)
    referral_code = models.CharField(max_length=50, null=True, blank=True)
    terms_and_condition = models.BooleanField(null=False, blank=False)


    # add rider uuid here
    def __str__(self):
        """
          String representation of the logistics partner
        """
        return "Rider: {} {}".format(self.user.name, self.identity_card_type)

