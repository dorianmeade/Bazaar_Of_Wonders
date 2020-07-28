from django.apps import AppConfig
import os


class MainConfig(AppConfig):
    name = 'main'

    # def ready(self):
    #     if os.environ.get('RUN_MAIN') != 'true':
    #         from main.scripts.notify import test
    #
    #         test(repeat=60)
