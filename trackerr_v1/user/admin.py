from django.contrib import admin
from .models import User, SMSSent

admin.site.register(User)
admin.site.register(SMSSent)
