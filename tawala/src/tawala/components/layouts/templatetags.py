"""Layout templatetags."""

from django.conf import settings
from django.template import Library

register = Library()


@register.simple_tag
def pkg_display_name() -> str:
    """Return the configured display name for the package."""
    return settings.PKG_DISPLAY_NAME
