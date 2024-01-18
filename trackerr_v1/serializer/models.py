from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=55)
    age = models.IntegerField()
    color = models.CharField()
