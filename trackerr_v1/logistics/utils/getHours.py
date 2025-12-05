from logistics.models import LogisticsOwnerStatusLog
from django.utils import timezone

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

    if last_active_time:
        total_seconds += (now - last_active_time).total_seconds()

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    return f"{hours}h {minutes}m"

