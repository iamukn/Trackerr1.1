from django.urls import path
from .views import views, business_owners_count

""" 
   Urls to handle requests for the Business owners
"""

urlpatterns = [
    path('business-owners/', views.GetAllBusinessOwners.as_view(), name='business-owners'),
    path('business-owners/signup/', views.Business_ownerRegistration.as_view(), name='business-owners-signup'),
    path('business-owners/<int:id>/', views.Business_ownerRoute.as_view(), name='business-owner-route'),
    path('business-owners-count/',business_owners_count.Business_count.as_view(), name='business-counts' ),
        ]
