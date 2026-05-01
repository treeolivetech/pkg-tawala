"""Core views."""

from django.views.generic.base import TemplateView


class WIPLayout(TemplateView):
    """Work in Progress page."""

    template_name = "wip/layout.html"
    extra_context: dict[str, bool | str] = {
        "site_title": "Work in Progress",
        "html_class": "m-0 p-0 h-100",
        "body_class": "m-0 p-0 h-100 bg-black",
    }
