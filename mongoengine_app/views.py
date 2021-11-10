from django.shortcuts import redirect
from rest_framework_mongoengine.generics import get_object_or_404
from .models import ShortLink


def short_link_redirect(request, pk):
    # NOTE: Using get_object_or_404 from rest_framework_mongoengine
    # here, because Django's native doesn't know about MongoEngine's
    # DoesNotExist exception, and hence will raise an error
    short_link = get_object_or_404(ShortLink.objects, pk=pk)
    return redirect(to=short_link.redirect_to, permanent=True)
