"""Layout templatetags."""

from django.conf import settings
from django.template import Library

register = Library()


@register.simple_tag
def base_display_name() -> str:
    """Return the configured display name for the package."""
    return settings.BASE_DISPLAY_NAME
