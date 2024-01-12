from django.contrib import admin
from .models import Books
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'message')



admin.site.register(Books, BookAdmin)
