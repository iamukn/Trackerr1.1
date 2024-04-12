#!/usr/bin/env python3
from datetime import date
from django.db import models
from user.models import User

""" Tracking model """

class Tracking_info(models.Model):
    parcel_number = models.CharField(max_length=15, unique=True, null=False, blank=False)
    date_of_purchase = models.DateField(auto_now_add=date.today, null=True, blank=True)
    delivery_date = models.DateField(default=date.today, null=False, blank=False) 
    shipping_address = models.CharField(max_length=255, null=False, blank=False)
    longitude = models.CharField(max_length=255, null=True, blank=True, default=None)
    latitude = models.CharField(max_length=255, null=True, blank=True, default=None)
    carrier_email = models.EmailField(null=True, blank=True, default=None)
    realtime_location = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=False, blank=False, default='Nigeria')
    product_name = models.CharField(max_length=255, null=False, blank=False, default='Unknown Product')
    quantity = models.IntegerField(null=False, blank=False, default=1)
    vendor = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=15, null=True, blank=True, default="Pending")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return f"{self.parcel_number}, {self.owner}, {self.country}, {self.vendor}, {self.status}"
