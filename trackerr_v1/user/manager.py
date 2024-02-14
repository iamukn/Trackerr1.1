from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_('Please enter a valid email address!'))

    def create_user(self, email, name, phone_number, address, account_type, password, **extra_fields):
        if email:
            email=self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_('An email address is required!'))

        if not name or not phone_number:
            raise ValueError(_('name or phone number is missing!'))

        user = self.model(email=email, name=name, phone_number=phone_number, address=address, account_type=account_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_number, address, account_type, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('admin user must also be a staff'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('is superuser must be True for admin user'))

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('is admin must be true for admin user'))

        user=self.create_user(
            email=email, name=name, phone_number=phone_number, address=address, account_type=account_type, password=password, **extra_fields    
                )

        user.save(using=self._db)

        return user
