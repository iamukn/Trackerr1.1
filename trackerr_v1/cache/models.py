from django.db import models

class Phone(models.Model):
    model = models.CharField(max_length=25, unique=True)
    imei = models.IntegerField()

# Create your models here.
