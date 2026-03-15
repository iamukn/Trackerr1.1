import math

def calc_distance(start_lat, start_lon, end_lat, end_lon):
    R = 6371  # Earth radius in km
    # Convert degrees to radians
    start_lat_rad, start_lon_rad = math.radians(start_lat), math.radians(start_lon)
    end_lat_rad, end_lon_rad = math.radians(end_lat), math.radians(end_lon)
    
    # Differences
    dlat = end_lat_rad - start_lat_rad
    dlon = end_lon_rad - start_lon_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(start_lat_rad) * math.cos(end_lat_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance
