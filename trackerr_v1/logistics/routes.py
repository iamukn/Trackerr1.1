from django.urls import path
from .views import logistics_users_count, update_riders_location
urlpatterns = [
    path('logistics-owners-count/', logistics_users_count.Logistics_owners_count.as_view(), name='logistics-count'),
    path('update-location/', update_riders_location.UpdateLocation.as_view(), name='realtime-location'),
        ]
