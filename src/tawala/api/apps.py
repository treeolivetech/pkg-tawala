"""api configuration."""

from django.apps import AppConfig as BaseAppConfig

from .. import DefaultApps


class ApiConfig(BaseAppConfig):
    """api configuration."""

    name = DefaultApps.API
