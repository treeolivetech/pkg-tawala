"""Work in Progress views."""

from django.views.generic.base import TemplateView


class WorkInProgressLayout(TemplateView):
    """Work in Progress page."""

    template_name = "core/wip.html"
    extra_context: dict[str, bool | str] = {
        "vendor_aos": False,
        "vendor_bootstrap": False,
        "site_title": "Work in Progress",
        "site_favicon": "core/wip/favicon.ico",
    }
