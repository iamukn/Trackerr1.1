from django.urls import path
from .views import views

""" 
   Urls to handle requests for the Business owners
"""

urlpatterns = [
    path('business-owners/', views.Business_ownerRegistration.as_view(), name='business-owners'),
    path('business-owner/<int:id>/', views.Business_ownerRoute.as_view(), name='business-owner-route'),
        ]
