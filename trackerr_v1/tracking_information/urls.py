#!/usr/bin/python3

from django.urls import path
from .views import generate_tracking_view, retrieve_all_tracking

""" tracking routes """

urlpatterns = [
    path('generate-tracking/', generate_tracking_view.GenerateView.as_view(), name='generate-tracking'),
    path('retrieve-all/', retrieve_all_tracking.RetrieveAllView.as_view(), name='retrieve-all'),
        ]
