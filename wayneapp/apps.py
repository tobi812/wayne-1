from django.apps import AppConfig
from wayne import settings


class WayneappConfig(AppConfig):
    name = settings.APP_LABEL


class JsonSchemaConfig(AppConfig):
    name = settings.APP_LABEL + '.' + settings.SCHEMA_APP_LABEL
    #label = settings.APP_LABEL+'.'+settings.SCHEMA_APP_LABEL
