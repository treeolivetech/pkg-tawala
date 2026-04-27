"""Widget template tags."""

from django.apps import apps
from django.conf import settings
from django.template import Context, Library
from django.template.loader import render_to_string

register = Library()


def _render_widget(widget_name: str, context: Context) -> str:
    """Render a widget if it is installed."""
    if apps.is_installed(f"{settings.WIDGET_APPS}.{widget_name}"):
        return render_to_string(f"{widget_name}/widget.html", context.flatten())
    return ""


@register.simple_tag(takes_context=True)
def widget_preloader(context: Context) -> str:  # noqa: D103
    return _render_widget("preloader", context)


@register.simple_tag(takes_context=True)
def widget_logout(context: Context) -> str:  # noqa: D103
    return _render_widget("logout", context)


@register.simple_tag(takes_context=True)
def widget_scroll_top(context: Context) -> str:  # noqa: D103
    return _render_widget("scroll_top", context)


@register.simple_tag(takes_context=True)
def widget_header(context: Context) -> str:  # noqa: D103
    return _render_widget("header", context)


@register.simple_tag(takes_context=True)
def widget_footer(context: Context) -> str:  # noqa: D103
    return _render_widget("footer", context)
