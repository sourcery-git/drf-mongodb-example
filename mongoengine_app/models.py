import mongoengine
from django.utils.crypto import get_random_string
from .apps import MongoengineAppConfig


class RandomStringPKDocument(mongoengine.Document):
    id = mongoengine.StringField(
        primary_key=True,
        max_length=12,
        default=get_random_string,
    )

    # Meta abstract
    meta = {'abstract': True}


class Account(RandomStringPKDocument):
    email = mongoengine.EmailField(required=True, unique=True)

    # Meta collection name
    meta = {'collection': f'{MongoengineAppConfig.name}_account'}


class ShortLink(RandomStringPKDocument):
    account = mongoengine.ReferenceField(
        Account,
        required=True,
        reverse_delete_rule=mongoengine.CASCADE,
    )
    redirect_to = mongoengine.URLField(required=True)

    # Meta collection name
    meta = {'collection': f'{MongoengineAppConfig.name}_shortlink'}
