from django.urls import path
from .views import (logistics_users_count,
                    update_riders_location,
                    create_rider,
                    read_update_delete_rider,
                    get_all_business_owners_riders,
                    fetch_tracking_info_linked_to_rider as rider
                    )
urlpatterns = [
    path('logistics/signup/', create_rider.RegisterRider.as_view(), name='logistics-signup'),
    path('logistics/riders/<int:id>/', read_update_delete_rider.Rider.as_view(), name='get-rider'),
    path('logistics/business-owners/riders/', get_all_business_owners_riders.Business_Riders.as_view(), name='get-business-owners-rider'),
    path('logistics-owners-count/', logistics_users_count.Logistics_owners_count.as_view(), name='logistics-count'),
    path('logistics-owners/update-location/', update_riders_location.UpdateLocation.as_view(), name='realtime-location'),
    path('rider/deliveries/', rider.Rider_history.as_view(), name='rider_orders')
        ]
