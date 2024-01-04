from django.db import models



class Books(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    isbn = models.CharField(max_length=50, blank=False, null=False)
    chapter = models.IntegerField(default=0, blank=False, null=False)


class Author(models.Model):
    relationship = models.OneToOneField(Books, on_delete=models.CASCADE)
    is_softcopy = models.BooleanField(default=False, null=False, blank=False)
