from django.db import models
from django.contrib.auth.models import User


class Tracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracking_num = models.CharField(max_length=30, null=False, blank=False)
    status1 = models.CharField(max_length=10, null=False, blank=False, default='Pending')
    status2 = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.tracking_num
    class Meta:
        ordering = ['tracking_num']
