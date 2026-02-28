import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackerr_v1.settings')

app = Celery('trackerr_v1')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



# Scheduled tasks
@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    from shared.celery_tasks.scheduled_tasks.rider_tasks import handle_rider_status
    sender.add_periodic_task(10.0, handle_rider_status.s(), name='check if a rider is still online every 30s')
