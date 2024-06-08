#!/usr/bin/python3

from django.urls import path
from .views import (
        generate_tracking_view,
        retrieve_all_tracking,
        retrieve_one,
        retrieve_status_count,
        track_a_parcel_realtime,
        get_activity_chart,
        fetch_tracking_info_using_customer_email,
        )

""" tracking routes """

urlpatterns = [
    path('generate-tracking/', generate_tracking_view.GenerateView.as_view(), name='generate-tracking'),
    path('tracking/realtime/', track_a_parcel_realtime.RealtimeParcelTracking.as_view(), name='realtime-tracking'),
    path('tracking/<str:num>/', retrieve_one.RetrieveOne.as_view(), name='track-one'),
    path('trackings/', retrieve_all_tracking.RetrieveAllView.as_view(), name='trackings'),
    path('trackings/history/', fetch_tracking_info_using_customer_email.Customer_history.as_view(), name='history'),
    path('trackings/status-count/', retrieve_status_count.RetrieveStatusCount.as_view(), name='status-count'),
    path('trackings/charts/weekly/', get_activity_chart.GetWeeklyActivityChart.as_view(), name='weekly-activity'),
    path('trackings/charts/monthly/', get_activity_chart.GetMonthlyActivityChart.as_view(), name='monthly-activity'),
        ]
