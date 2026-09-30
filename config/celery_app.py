import os
from celery import Celery
from django.conf import settings

# Set default settings for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings.local")  # set to config.settings.production in production

app = Celery("accomm_mngmt")

# Load settings from Django settings file
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed Django apps
# lambda:settings.INSTALLED_APPS
app.autodiscover_tasks()

@app.task(name="tasks.debug_task")
def debug_task():
    print("Debug task executed!")
