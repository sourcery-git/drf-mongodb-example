import mongoengine
from django.apps import AppConfig


class MongoengineAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mongoengine_app'
