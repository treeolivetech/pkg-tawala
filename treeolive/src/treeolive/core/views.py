"""Core views."""

from django.views.generic.base import TemplateView


class Handler404(TemplateView):
    """Custom 404 error handler view."""

    template_name = "core/404.html"
