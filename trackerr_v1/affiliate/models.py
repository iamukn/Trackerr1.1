import uuid
from django.db import models
from affiliate.utils.generate_referral_code import generate_referral_code


class Affiliate(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    referral_code = models.CharField(null=False, blank=False, unique=True, default=generate_referral_code)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    total_coins_withdrawn = models.IntegerField(default=0)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email


class AffiliateOTP(models.Model):
    affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.CASCADE,
        related_name="otps",
    )
    otp_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class AffiliateSession(models.Model):
    affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    token_hash = models.CharField(max_length=128, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

class AccountDetails(models.Model):
    affiliate = models.ForeignKey(
            Affiliate,
            on_delete=models.CASCADE,
            related_name="account_details",
            )

    bank_name = models.CharField(max_length=128, null=True, blank=True)
    account_number = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
