"""ui templatetags."""

from django.apps import apps
from django.template import Context, Library
from django.template.loader import render_to_string

from .conf import (
    ASSET_AOS,
    ASSET_BOOTSTRAP,
    WIDGET_FOOTER,
    WIDGET_HEADER,
    WIDGET_PRELOADER,
    WIDGET_SCROLL_TOP,
)

register = Library()


def _render_ui(module: str, component: str, context: Context) -> str:
    """Render component if it is installed."""
    if apps.is_installed(module):
        return render_to_string(f"{component}/component.html", context.flatten())
    return ""


_WIDGETS = {
    "preloader": WIDGET_PRELOADER,
    "scroll_top": WIDGET_SCROLL_TOP,
    "header": WIDGET_HEADER,
    "footer": WIDGET_FOOTER,
}

_ASSETS = {
    "aos": ASSET_AOS,
    "bootstrap": ASSET_BOOTSTRAP,
}


@register.simple_tag(takes_context=True)
def widget(context: Context, name: str) -> str:
    """Render widget by name."""
    module = _WIDGETS.get(name)
    if not module:
        raise ValueError(f"Unknown widget: {name}")
    return _render_ui(module, name, context)


@register.simple_tag(takes_context=True)
def asset(context: Context, name: str) -> str:
    """Render asset by name."""
    module = _ASSETS.get(name)
    if not module:
        raise ValueError(f"Unknown asset: {name}")
    return _render_ui(module, name, context)
