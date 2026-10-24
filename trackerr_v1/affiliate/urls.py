from django.urls import path
from affiliate.views.create_affiliate import CreateAffiliate
from affiliate.views.request_otp import RequestOTP
from affiliate.views.auth import Login, Logout
from affiliate.views.get_affiliate import GetAffiliate
from affiliate.views.get_referrals import GetReferrals
from affiliate.views.add_bank_details import AccountDetails, Banks


urlpatterns = [
    path('create/', CreateAffiliate.as_view(), name='create-affiliate'),
    path('request-otp/', RequestOTP.as_view(), name='request-otp'),
    path('authenticate/', Login.as_view(), name='authenticate'),
    path('user/', GetAffiliate.as_view(), name='get-affiliate-user'),
    path('all-banks/', Banks.as_view(), name='get-banks'),
    path('bank-account/', AccountDetails.as_view(), name="bank-account"),
    path('referrals/', GetReferrals.as_view(), name='affiliated-business'),
    path('logout/', Logout.as_view(), name='logout')
        ]
