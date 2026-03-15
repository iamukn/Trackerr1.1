def calculate_eta(distance_km, speed_kmh):
    eta_hours = distance_km / speed_kmh
    eta_mins = int(eta_hours * 60)


    if eta_mins < 60:
        return f"{eta_mins}m"

    hours = eta_mins // 60
    mins = eta_mins % 60
    if hours == 1:
        return f"{hours}hr:{mins}mins"
    return f"{hours}hrs:{mins}mins"
