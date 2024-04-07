#!/usr/bin/python3

from django.urls import path
from .views import generate_tracking_view, retrieve_all_tracking, retrieve_one, retrieve_status_count

""" tracking routes """

urlpatterns = [
    path('generate-tracking/', generate_tracking_view.GenerateView.as_view(), name='generate-tracking'),
    path('tracking/<str:num>/', retrieve_one.RetrieveOne.as_view(), name='track-one'),
    path('trackings/', retrieve_all_tracking.RetrieveAllView.as_view(), name='trackings'),
    path('trackings/status-count/', retrieve_status_count.RetrieveStatusCount.as_view(), name='status-count'),
        ]
