"""Core views."""

from django.views.generic.base import TemplateView


class WorkInProgressLayout(TemplateView):
    """Work in Progress page."""

    template_name = "wip/layout.html"
    extra_context: dict[str, bool | str] = {
        "site_title": "Work in Progress",
    }
