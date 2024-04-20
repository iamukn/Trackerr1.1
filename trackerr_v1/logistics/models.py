from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
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

    def __str__(self):
        """
          String representation of the logistics partner
        """
        return "Logistics Partner model"

