"""
WSGI config for bazaar_of_wonders project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import datetime
from django.core.wsgi import get_wsgi_application
from apscheduler.schedulers.background import BackgroundScheduler
from main.scripts.notify import update_data

WSGI_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
scheduler = BackgroundScheduler()

scheduler.start()

os.chdir( WSGI_FILE_DIR +  "/../main/scripts")

# Set to update the data every day at 1 AM EST
scheduler.add_job(update_data, 'cron', day='*', hour=5, id='update_data', replace_existing=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazaar_of_wonders.settings')

application = get_wsgi_application()
