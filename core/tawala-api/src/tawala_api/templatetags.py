"""API templatetags."""

from django.template import Library

from .apps import PROJECT_API

register = Library()


@register.simple_tag
def pkg_display_name() -> str:
    """Return the configured display name for the package."""
    return PROJECT_API.pkg_display_name
