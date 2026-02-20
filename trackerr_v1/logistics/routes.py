from django.urls import path
from .views import (logistics_users_count,
                    update_riders_location,
                    update_rider_status,
                    create_rider,
                    read_update_delete_rider,
                    get_all_business_owners_riders,
                    fetch_tracking_info_linked_to_rider as rider,
                    get_hours_today,
                    broadcast_riders_location as broadcast,
                    )
from tracking_information.views import fetch_deliveries

urlpatterns = [
    path('rider/location/broadcast', broadcast.BroadcastLocation.as_view(), name='rider_location_broadcast'),
    path('logistics/signup/', create_rider.RegisterRider.as_view(), name='logistics-signup'),
    path('logistics/riders/<int:id>/', read_update_delete_rider.Rider.as_view(), name='get-rider'),
    path('logistics/business-owners/riders/', get_all_business_owners_riders.Business_Riders.as_view(), name='get-business-owners-rider'),
    path('logistics-owners-count/', logistics_users_count.Logistics_owners_count.as_view(), name='logistics-count'),
    path('logistics/riders/status-update/', update_rider_status.RiderStatus.as_view(), name='update-status'),
    path('logistics-owners/update-location/', update_riders_location.UpdateLocation.as_view(), name='realtime-location'),
    path('logistics/rider/deliveries/', fetch_deliveries.GetDeliveries.as_view(), name='deliveries'),
    path('logistics/riders/get-hours/', get_hours_today.GetHoursToday.as_view(), name='get-hours'),
    path('rider/deliveries/', rider.Rider_history.as_view(), name='rider_orders'),
        ]
