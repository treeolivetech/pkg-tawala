"""WIP views."""

from django.views.generic.base import TemplateView


class WorkInProgressView(TemplateView):
    """Work in Progress page."""

    template_name = "work_in_progress/index.html"
