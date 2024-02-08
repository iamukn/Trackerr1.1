from django.db import models
from django.contrib.postgres.fields import ArrayField

class Department(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):

        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=35, null=False, blank=False)
    age = models.IntegerField(default=0)
    department = models.OneToOneField(Department, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name

class Animal(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
   # kinds = ArrayField(models.CharField(max_length=10), default=list)
    def __str__(self):
        return self.name


class Species(models.Model):
    name = models.CharField(max_length=35, null=False, blank=False)
    age = models.IntegerField(default=0)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
