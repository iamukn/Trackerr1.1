#!/usr/bin/env python3
from datetime import date
import time
from django.db import models
from logistics.models import Logistics_partner
from user.models import User

""" Tracking model """

class Tracking_info(models.Model):
    parcel_number = models.CharField(max_length=15, unique=True, null=False, blank=False)
    date_of_purchase = models.DateField(auto_now_add=date.today, null=False, blank=False)
    time_of_purchase = models.CharField(default=time.strftime('%H:%M' + 'hrs'), null=False, blank=False)
    customer_email = models.CharField(max_length=255, null=True, blank=True)
    delivery_date = models.DateField(default=date.today, null=False, blank=False) 
    shipping_address = models.CharField(max_length=255, null=False, blank=False)
    latitude = models.CharField(max_length=255, null=True, blank=True, default=None)
    longitude = models.CharField(max_length=255, null=True, blank=True, default=None)
    destination_lat = models.CharField(max_length=255, null=False, blank=False)
    destination_lng = models.CharField(max_length=255, null=False, blank=False)
    rider = models.ForeignKey(Logistics_partner, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    rider_email = models.EmailField(max_length=255,null=True, blank=True, default=None)
    realtime_location = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=False, blank=False, default='Nigeria')
    product_name = models.CharField(max_length=255, null=False, blank=False, default='Unknown Product')
    quantity = models.IntegerField(null=False, blank=False, default=1)
    status = models.CharField(max_length=15, null=True, blank=True, default="Pending")
    vendor = models.CharField(max_length=255, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return f"{self.parcel_number}, {self.owner}, {self.country}, {self.vendor}, {self.status}"
