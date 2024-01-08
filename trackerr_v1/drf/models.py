from django.db import models

class Books(models.Model):
    author = models.CharField(null=False, blank=False, max_length=50)
    message = models.CharField(null=False, blank=False, max_length=50)

    class Meta:
        verbose_name = 'books'

# Create your models here.
