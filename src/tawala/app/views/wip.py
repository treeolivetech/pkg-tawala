"""Views for the WIP app."""

from django.views.generic.base import TemplateView

__all__ = ["WIPView"]


class WIPView(TemplateView):
    """Work in Progress page."""

    template_name = "wip/index.html"
