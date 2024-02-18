from django.urls import path
from . import views

""" 
   Urls to handle requests for the Business owners
"""

urlpatterns = [
    path('business-owners/', views.Business_ownerRegistration.as_view(), name='busines-owners'),
    path('business-owners/<int:id>/', views.Business_ownerRoute.as_view(), name='busines-owners-route'),
        ]