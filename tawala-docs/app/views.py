"""Views for the tawala-docs app."""

from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    """Render the home page."""

    template_name = "app/layout.html"
