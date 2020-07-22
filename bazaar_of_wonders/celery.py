import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bazaar_of_wonders.settings")

app = Celery("bazaar_of_wonders")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
