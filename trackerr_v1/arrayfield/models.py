from django.db import models
from django.contrib.postgres.fields import ArrayField

class Arr(models.Model):
    track = ArrayField(models.CharField(), default=list)

# Create your models here.
