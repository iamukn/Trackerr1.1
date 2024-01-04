from django.db import models




class Author(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    is_softcopy = models.BooleanField(default=False, null=False, blank=False)
    def __str__(self):
        return f"{self.name} is the authors name"

class Books(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    isbn = models.CharField(max_length=50, blank=False, null=False)
    chapter = models.IntegerField(default=0, blank=False, null=False)
    relationship = models.OneToOneField(Author, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s is the relationship" % self.relationship
