from django.urls import path
from .views import views, business_owners_count

""" 
   Urls to handle requests for the Business owners
"""

urlpatterns = [
    path('business-owners/', views.Business_ownerRegistration.as_view(), name='business-owners'),
    path('business-owner/<int:id>/', views.Business_ownerRoute.as_view(), name='business-owner-route'),
    path('business-owner-count/',business_owners_count.Business_count.as_view(), name='business-counts' ),
        ]
