from django.contrib import admin
from .models import (User, Logistics_partner, Business_owner)

admin.site.register(User)
admin.site.register(Logistics_partner)
admin.site.register(Business_owner)
