#!/usr/bin/env python3
from datetime import date
import time
from django.utils import timezone
from django.db import models
from logistics.models import Logistics_partner
from user.models import User

""" Tracking model """

def get_current_time_str():
    return timezone.now().strftime('%H:%Mhrs')

class Tracking_info(models.Model):
    parcel_number = models.CharField(max_length=15, unique=True, null=False, blank=False)
    date_of_purchase = models.DateField(auto_now_add=date.today, null=False, blank=False)
    time_of_purchase = models.CharField(default=get_current_time_str, null=False, blank=False)
    #time_of_purchase = models.TimeField(auto_now_add=True)
    customer_email = models.CharField(max_length=255, null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    delivery_date = models.DateField(default=date.today, null=False, blank=False) 
    shipping_address = models.CharField(max_length=255, null=False, blank=False)
  # latitude = models.CharField(max_length=255, null=True, blank=True, default=None)
  # longitude = models.CharField(max_length=255, null=True, blank=True, default=None)
    is_assigned = models.BooleanField(null=False, blank=False, default=False)
    destination_lat = models.CharField(max_length=255, null=False, blank=False)
    destination_lng = models.CharField(max_length=255, null=False, blank=False)
    business_owner_lat = models.CharField(max_length=30, null=True, blank=True)
    business_owner_lng = models.CharField(max_length=30, null=True, blank=True)
    rider = models.ForeignKey(Logistics_partner, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    rider_email = models.EmailField(max_length=255,null=True, blank=True, default=None)
    rider_uuid = models.CharField(max_length=500, null=True, blank=True)
    rider_lat = models.CharField(max_length=30, null=True, blank=True)
    rider_lng = models.CharField(max_length=30, null=True, blank=True)
    rider_name = models.CharField(max_length=200, null=True, blank=True)
    rider_phone = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=255, null=False, blank=False, default='Nigeria')
    product_name = models.CharField(max_length=255, null=False, blank=False, default='unknown product')
    quantity = models.IntegerField(null=False, blank=False, default=1)
    status = models.CharField(max_length=15, null=True, blank=True, default="pending")
    vendor = models.CharField(max_length=255, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return f"{self.parcel_number}, {self.owner}, {self.country}, {self.vendor}, {self.status}"
