"""[BASE_CONF_IMPORT_ALLOWED_PREINIT] Apps."""

from django.apps import AppConfig

from ..settings.conf import BASE_CONF


class AppsConfig(AppConfig):
    """Apps module."""

    name = BASE_CONF.pkg_name

    def ready(self) -> None:
        """Configure the admin site."""
        from django.contrib.admin import site

        site.site_header = f"{BASE_CONF.pkg_display_name} administration"
        site.site_title = f"{BASE_CONF.pkg_display_name} Admin Portal"
