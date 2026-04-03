"""app configuration."""

from django.apps import AppConfig as BaseAppConfig

from .. import DefaultApps


class AppConfig(BaseAppConfig):
    """app configuration."""

    name = DefaultApps.APP
