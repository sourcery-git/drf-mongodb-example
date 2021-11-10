from django.utils.crypto import get_random_string
from djongo import models


class Account(models.Model):
    email = models.EmailField()


class ShortLink(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=12,
        default=get_random_string,
    )
    # FK into Account to define ownership
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='short_links',
    )
    # Where this short link will redirect to
    redirect_to = models.URLField()
