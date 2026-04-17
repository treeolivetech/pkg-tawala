"""Apps."""

from django.apps import AppConfig
from django.conf import settings


class AppsConfig(AppConfig):
    """Apps module."""

    name = settings.PKG_NAME

    def ready(self) -> None:
        """Configure the admin site."""
        from django.contrib.admin import site

        site.site_header = f"{settings.PKG_DISPLAY_NAME} administration"
        site.site_title = f"{settings.PKG_DISPLAY_NAME} Admin Portal"
