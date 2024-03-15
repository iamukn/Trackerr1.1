#!/usr/bin/python3

from django.urls import path
from .views import generate_tracking_view

""" tracking routes """

urlpatterns = [
    path('generate-tracking/', generate_tracking_view.GenerateView.as_view(), name='generate-tracking'),
        ]
