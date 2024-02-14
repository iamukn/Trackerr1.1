from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
"""
Custom user model to handle registration of both Business user and Logistics Partner
"""


class User(AbstractBaseUser, PermissionsMixin):
    """ User Model fields to serve as the base user for both Business owner
    and Logistics partner
    """
    name = models.CharField(max_length=500, null=False, blank=False, verbose_name=_('Name'))
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True, verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name=_('Phone'))
    address = models.CharField(max_length=500, null=False, blank=False, verbose_name=_('Address'))
    account_type = models.CharField(max_length=15, null=False, blank=False, verbose_name=_('account_type'))
    logo = models.ImageField(null=True, blank=True, upload_to="images/")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'phone_number', 'address', 'account_type']

    objects = UserManager()

    def __str__(self):
        """ string representation of the
        User model.
        Args:
            self: the model itself
        Return:
            The created instance name
        """
        return self.name


class Logistics_partner(models.Model):
    """ Model that relatates the User to Logistics partner
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """ string representation of the
        logistics partner 
        """
        return "Logistics Partner model"


class Business_owner(models.Model):
    """ Model that relatates the User to Business owner
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=200, null=False, blank=False, verbose_name=_('services'), default='Parcel Delivery')
    business_name = models.CharField(max_length=500, null=False, blank=False, unique=True, verbose_name=_('Business name'))

    def __str__(self):
        """ string representation of the
        business owner 
        Args:
            self: The model instance itself
        Return:
            The Business owner
        """
        return "Business owner model"
