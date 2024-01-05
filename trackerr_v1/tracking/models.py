from django.db import models
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Tracking(models.Model):
    tracking_num = ArrayField(models.CharField(max_length=100), size=4)

# Create your models here.
