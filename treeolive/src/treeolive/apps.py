"""Core app."""

from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    """Core app."""

    name = settings.CORE_APP

    def ready(self) -> None:
        """Configure the admin site."""
        from django.contrib.admin import site

        site.site_header = f"{settings.CORE_DISPLAY_NAME} administration"
        site.site_title = f"{settings.CORE_DISPLAY_NAME} Admin Portal"
