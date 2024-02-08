from django.db import models

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


class Species(models.Model):
    name = models.CharField(max_length=35, null=False, blank=False)
    age = models.IntegerField(default=0)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
