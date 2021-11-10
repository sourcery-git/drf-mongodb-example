from django.shortcuts import get_object_or_404, redirect
from .models import ShortLink


def short_link_redirect(request, pk):
    short_link = get_object_or_404(ShortLink, pk=pk)
    return redirect(to=short_link.redirect_to, permanent=True)
