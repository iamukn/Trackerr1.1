#!/usr/bin/python3

from django.urls import path
from .views import update_location

# Web socket routes
websocket_urlpatterns = [
    path("ws/rider-update/", update_location.RiderLocationConsumer.as_asgi()),
]
