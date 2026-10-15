from django.db import models

# Create your models here.


class WhatsappNotification(models.Model):
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True,blank=True)
    read_at = models.DateTimeField(null=True,blank=True)
    sender_phone = models.CharField(max_length=21, null=True, blank=True)
    receiver_phone = models.CharField(max_length=21, null=True, blank=True)
    category = models.CharField(max_length=21, null=False, blank=False, default='utility')
    user_id = models.CharField(max_length=100, null=True, blank=True)
    message_status = models.CharField(max_length=15, null=False, blank=False, default="sent") # sent -> delivered | failed
    message_status_id = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.CharField(max_length=40, null=True, blank=True)
    billable = models.BooleanField(null=False, blank=False, default=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    parcel_number = models.CharField(max_length=20, null=True, blank=True)
    parcel_status = models.CharField(max_length=12, null=True, blank=True) # assigned -> in transit -> delivered | returned 



    def __str__(self):
        return f"{self.parcel_number.upper()}-{self.parcel_status}-{self.message_status}"
