#!/usr/bin/env python3
from datetime import date
from django.db import models

""" Tracking model """

class Tracking(models.Model):
    parcel_number = models.CharField(max_length=15, null=False, blank=False)
    date_of_purchase = models.DateField(default=date.today, null=False, blank=False)
    delivery_date = models.DateField(default=date.today, null=False, blank=False) 
    shipping_address = models.CharField(max_length=255, null=False, blank=False)
    vendor = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=15, null=False, blank=False, default="Pending")

    class Meta:
        verbose_name = 'tracking'
