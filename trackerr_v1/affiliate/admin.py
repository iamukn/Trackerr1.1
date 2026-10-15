from django.contrib import admin
from affiliate.models import Affiliate, AffiliateOTP, AffiliateSession, AccountDetails
# Register your models here.

admin.site.register(Affiliate)
admin.site.register(AccountDetails)
admin.site.register(AffiliateOTP)
admin.site.register(AffiliateSession)
