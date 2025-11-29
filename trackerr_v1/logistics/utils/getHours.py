from django.utils import timezone
from logistics.models import LogisticsOwnerStatusLog

def get_today_active_hours(rider):
    now = timezone.now()
    today = now.date()

    logs = LogisticsOwnerStatusLog.objects.filter(
        rider=rider,
        timestamp__date=today
    ).order_by("timestamp")

    total_seconds = 0
    last_active_time = None

    for log in logs:
        if log.status == "active":
            last_active_time = log.timestamp
        elif log.status == "inactive" and last_active_time:
            total_seconds += (log.timestamp - last_active_time).total_seconds()
            last_active_time = None

    # If rider is STILL active right now
    if last_active_time:
        total_seconds += (now - last_active_time).total_seconds()

    hours = total_seconds / 3600
    return round(hours, 2)  # e.g. 6.5 hours
