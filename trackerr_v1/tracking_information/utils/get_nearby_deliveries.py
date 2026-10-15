from math import radians, sin, cos, sqrt, atan2

from tracking_information.models import Tracking_info
from logistics.models import Logistics_partner


def calculate_distance(lat1, lng1, lat2, lng2):
    """
    Calculate distance between two coordinates in kilometers.
    """
    R = 6371  # Earth's radius in km

    lat1 = radians(float(lat1))
    lng1 = radians(float(lng1))
    lat2 = radians(float(lat2))
    lng2 = radians(float(lng2))

    dlat = lat2 - lat1
    dlng = lng2 - lng1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_nearby_deliveries(
    parcel_data: dict,
    rider: Logistics_partner,
    radius_km: float = 2.0
) -> list:

    nearby = []

    # Coordinates of the parcel currently being delivered
    current_lat = parcel_data.get("destination_lat")
    current_lng = parcel_data.get("destination_lng")

    if not current_lat or not current_lng:
        return nearby

    current_lat = float(current_lat)
    current_lng = float(current_lng)

    # Get other parcels assigned to the same rider
    deliveries = Tracking_info.objects.filter(
        rider=rider,
        status__in=["assigned", "in transit"]
    ).exclude(
        parcel_number=parcel_data.get("parcel_number")
    )

    for delivery in deliveries:

        if not delivery.destination_lat or not delivery.destination_lng:
            continue

        distance = calculate_distance(
            current_lat,
            current_lng,
            delivery.destination_lat,
            delivery.destination_lng
        )

        if distance <= radius_km:

#            nearby.append({
#                "id": delivery.id,
#                "parcel_number": delivery.parcel_number,
#                "customer_name": delivery.customer_name,
#                "shipping_address": delivery.shipping_address,
#                "destination_lat": delivery.destination_lat,
#                "destination_lng": delivery.destination_lng,
#                "distance": round(distance, 2),
#                "status": delivery.status,
#            })
            nearby.append(delivery.parcel_number)
    # Closest destinations first
#   nearby.sort(key=lambda x: x["distance"])

    print('NEARBY"::::', nearby)

    return nearby
