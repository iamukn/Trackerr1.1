from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from datetime import datetime, timedelta, date

class Trackings(models.Model):
    parcel_num = models.CharField(max_length=50, null=False, blank=False)
  #  tracking_num = ArrayField(models.CharField(max_length=100), size=4, null=True)
    date_of_purchase = models.DateTimeField(default=timezone.now)
    shipping_address = models.CharField(max_length=300, null=False, blank=False)
    estimated_delivery_date = models.DateField(default=date.today)
    vendor = models.CharField(null=False, blank=False, max_length=500)
    status = models.CharField(null=False, blank=False, default='Pending')
# Create your models here.
