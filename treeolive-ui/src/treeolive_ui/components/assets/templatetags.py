"""Vendor template tags."""

from django.apps import apps
from django.conf import settings
from django.template import Context, Library
from django.template.loader import render_to_string

register = Library()


def _render_asset(asset_name: str, context: Context) -> str:
    """Render an asset if it is installed."""
    if apps.is_installed(f"{settings.ASSET_APPS}.{asset_name}"):
        return render_to_string(f"{asset_name}/asset.html", context.flatten())
    return ""


@register.simple_tag(takes_context=True)
def asset_aos(context: Context) -> str:
    """Render AOS vendor assets."""
    return _render_asset("aos", context)


@register.simple_tag(takes_context=True)
def asset_bootstrap(context: Context) -> str:
    """Render Bootstrap vendor assets."""
    return _render_asset("bootstrap", context)
