from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User 

"""
  Models that links the business owner to a User

"""

class Business_owner(models.Model):
    """
      Model that relatates the User to Business owner
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=200, null=False, blank=False, verbose_name=_('services'), default='Parcel Delivery')
    business_name = models.CharField(max_length=500, null=False, blank=False, unique=True, verbose_name=_('Business name'))

    def __str__(self):
        """ string representation of the business owner
        Args:
            self: The model instance itself
        Return:
            The Business owner
        """
        return "Business owner model"
