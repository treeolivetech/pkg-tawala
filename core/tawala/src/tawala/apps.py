"""Base app."""

from django.apps import AppConfig
from django.conf import settings


class BaseConfig(AppConfig):
    """Base app."""

    name = settings.BASE_APP

    def ready(self) -> None:
        """Configure the admin site."""
        from django.contrib.admin import site

        site.site_header = f"{settings.BASE_DISPLAY_NAME} administration"
        site.site_title = f"{settings.BASE_DISPLAY_NAME} Admin Portal"
