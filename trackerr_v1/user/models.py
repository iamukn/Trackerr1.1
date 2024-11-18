from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta
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

class Otp(models.Model):
    # otp model
    hashed_otp = models.CharField(max_length=128, default=None, null=True, blank=True, unique=False, verbose_name=_('otp'))
    otp_expiration = models.DateTimeField(null=True, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """ string representation of the
        otp owners
        """
        return "{} otps model".format(self.owner.email)

    def set_otp(self, otp):
        # set the password
        self.hashed_otp = make_password(otp)
        self.otp_expiration = now() + timedelta(minutes=15)
        
    def check_otp(self, otp):
        # check otp
        otp_expired = self.otp_expiration > now()
        check_pword = check_password(otp, self.hashed_otp)
        return check_pword and otp_expired
