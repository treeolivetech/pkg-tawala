"""app template tags."""

from django.template import Library

from ... import Package

register = Library()


@register.simple_tag
def pkg_display_name() -> str:
    """Return the configured display name for the package."""
    return Package.DISPLAY_NAME
