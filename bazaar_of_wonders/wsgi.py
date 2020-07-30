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
from main.scripts.notify import update_data, send_email_notif


scheduler = BackgroundScheduler()

scheduler.start()

os.chdir("./main/scripts")

# Set to update the data every day at midnight
scheduler.add_job(update_data, 'cron', day='*', id='update_data', replace_existing=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazaar_of_wonders.settings')

application = get_wsgi_application()
