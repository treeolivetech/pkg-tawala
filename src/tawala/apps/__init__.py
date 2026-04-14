"""Apps module."""

from django.apps import AppConfig

from .. import CONF


class TawalaConfig(AppConfig):
    """App module."""

    name = CONF.pkg_name

    def ready(self) -> None:
        """Configure the admin site."""
        from django.contrib.admin import site

        site.site_header = f"{CONF.pkg_display_name} administration"
        site.site_title = f"{CONF.pkg_display_name} Admin Portal"
