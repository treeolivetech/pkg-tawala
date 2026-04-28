"""Widget templatetags for tawala_ui widgets."""

from django.apps import apps
from django.template import Context, Library
from django.template.loader import render_to_string

from ..apps import (
    WIDGET_FOOTER,
    WIDGET_HEADER,
    WIDGET_LOGOUT,
    WIDGET_PRELOADER,
    WIDGET_SCROLL_TOP,
)

register = Library()

_WIDGETS = {
    "logout": WIDGET_LOGOUT,
    "preloader": WIDGET_PRELOADER,
    "scroll_top": WIDGET_SCROLL_TOP,
    "header": WIDGET_HEADER,
    "footer": WIDGET_FOOTER,
}


def _render_widget(module: str, widget: str, context: Context) -> str:
    """Render widget if it is installed."""
    if apps.is_installed(module):
        return render_to_string(f"{widget}/widget.html", context.flatten())
    return ""


@register.simple_tag(takes_context=True)
def widget(context: Context, name: str) -> str:
    """Render widget by name."""
    module = _WIDGETS.get(name)
    if not module:
        raise ValueError(f"Unknown widget: {name}")
    return _render_widget(module, name, context)
