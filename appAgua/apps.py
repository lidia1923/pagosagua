from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class AppaguaConfig(AppConfig):
    name = 'appAgua'

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'