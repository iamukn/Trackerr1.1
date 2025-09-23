#!/usr/bin/python3

from django.urls import path
from .views import track_a_parcel_realtime

# Web socket routes
websocket_urlpatterns = [
    path("ws/tracking/", track_a_parcel_realtime.RealtimeTracking.as_asgi()),
]
