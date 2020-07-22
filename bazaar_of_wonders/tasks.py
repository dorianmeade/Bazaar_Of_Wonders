from celery import shared_task
from django.core import management
from main.static.main.card_data.auto_parse_data import parse_data
from main.static.main.card_data.auto_get_data import get_data


@shared_task
def update_data():
    get_data()
    parse_data()
    print("New data retrieved")

    management.call_command('loaddata', 'cards.json', verbosity=0)
    print("Cards updated")
    management.call_command('loaddata', 'listings.json', verbosity=0)
    print("Listings updated")