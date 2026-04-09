from django.db import models
import uuid
from decimal import Decimal
from user.models import User

class Wallet(models.Model):
    # Primary Key as UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to user
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    
    # Balance using DecimalField (avoid float for money)
    balance = models.DecimalField(max_digits=18, decimal_places=8, default=Decimal('0.0'))
    
    # Currency as string or Enum
    CURRENCY_CHOICES = [
        ('NGN', 'Nigerian Naira'),
        ('GHC', 'Ghana Cedis'),
    ]
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='NGN')
    
    # Wallet status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('frozen', 'Frozen'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.owner.name} - {self.balance}{self.currency} Wallet"


class Payment(models.Model):


    STATUS_CHOICES = [
            ( 'pending', 'Pending' ),
            ('success', 'Success')
            ]
    email = models.EmailField(null=False, blank=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2,
            null=False, blank=False, 
            default=0.00)
    currency = models.CharField(max_length=5, null=False, blank=False, default='NGN')
    authorization_url = models.CharField(max_length=500, null=False, blank=False)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, null=False, blank=False, default='pending')
    payment_channel = models.CharField(max_length=25, null=True, blank=True)
    ip_address = models.CharField(max_length=25, null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    # fields for bank transfers, card deposits
    sender_name = models.CharField(max_length=100, null=True, blank=True)
    sender_account_number = models.CharField(max_length=15, null=True, blank=True)
    sender_country = models.CharField(max_length=5, null=True, blank=True)
    sender_bank = models.CharField(max_length=150, null=True, blank=True)
    sender_narration = models.CharField(max_length=255, null=True, blank=True)

    account_name = models.CharField(max_length=100, null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    exp_year = models.CharField(max_length=4, null=True, blank=True)
    exp_month = models.CharField(max_length=2, null=True, blank=True)
    card_type = models.CharField(max_length=15, null=True, blank=True)
    country_code = models.CharField(max_length=4, null=True, blank=True)
    # idempotency key
    idempotency_key = models.UUIDField(null=True, blank=True, unique=True)


    def __str__(self):
        return f'{self.email}: {self.amount}{self.currency}'
