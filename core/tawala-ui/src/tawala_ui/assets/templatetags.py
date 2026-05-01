"""Asset templatetags."""

from django.apps import apps
from django.template import Context, Library
from django.template.loader import render_to_string

from ..apps import (
    ASSET_AOS,
    ASSET_BOOTSTRAP,
)

register = Library()

_ASSETS = {
    "aos": ASSET_AOS,
    "bootstrap": ASSET_BOOTSTRAP,
}


def _render_asset(module: str, asset: str, context: Context) -> str:
    """Render asset if it is installed."""
    if apps.is_installed(module):
        return render_to_string(f"{asset}/asset.html", context.flatten())
    return ""


@register.simple_tag(takes_context=True)
def asset(context: Context, name: str) -> str:
    """Render asset by name."""
    module = _ASSETS.get(name)
    if not module:
        raise ValueError(f"Unknown asset: {name}")
    return _render_asset(module, name, context)
