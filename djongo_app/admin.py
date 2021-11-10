from django.contrib import admin
from .models import Account, ShortLink

admin.site.register([Account, ShortLink])
