from django.apps import AppConfig
# import os
# from main.static.main.card_data.auto_parse_data import parse_data
# from main.static.main.card_data.auto_get_data import get_data
# from django.core import management


class MainConfig(AppConfig):
    name = 'main'

#     def ready(self):
#         if os.environ.get('RUN_MAIN') != 'true':
#
#             # Updates card and listing data when app is initialized
#             # We should make sure this implementation works in production.
#             get_data()
#             parse_data()
#             print("New data retrieved")
#
#             management.call_command('loaddata', 'cards.json', verbosity=0)
#             print("Cards updated")
#             management.call_command('loaddata', 'listings.json', verbosity=0)
#             print("Listings updated")

