import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cond_observer_v2.settings')

app = Celery('cond_observer_v2', backend='db+postgresql://postgres:kriegsmarine@localhost:5432/co', broker='pyamqp://guest@localhost//')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_indicators_data': {
        'task': 'main.tasks.generate_data',
        'schedule': 1.0,
    }
}
