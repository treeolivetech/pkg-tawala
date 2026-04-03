"""Views for the WIP app."""

from django.views.generic.base import TemplateView


class WIPView(TemplateView):
    """Work in Progress page."""

    template_name = "wip/index.html"
