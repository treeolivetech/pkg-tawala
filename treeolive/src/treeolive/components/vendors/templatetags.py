"""Vendor template tags."""

from django.apps import apps
from django.conf import settings
from django.template import Context, Library
from django.template.loader import render_to_string

register = Library()


def _render_vendor(vendor_name: str, context: Context) -> str:
    """Render a vendor if it is installed."""
    if apps.is_installed(f"{settings.VENDORS_MODULE}.{vendor_name}"):
        return render_to_string(f"{vendor_name}/vendor.html", context.flatten())
    return ""


@register.simple_tag(takes_context=True)
def vendor_aos(context: Context) -> str:
    """Render AOS vendor assets."""
    return _render_vendor("aos", context)


@register.simple_tag(takes_context=True)
def vendor_bootstrap(context: Context) -> str:
    """Render Bootstrap vendor assets."""
    return _render_vendor("bootstrap", context)
