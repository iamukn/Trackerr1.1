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
        return f"{self.owner.name} - {self.currency} Wallet"

