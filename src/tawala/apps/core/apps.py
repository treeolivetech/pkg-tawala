"""Core app."""

from django.apps import AppConfig

from ... import CONF


class CoreConfig(AppConfig):
    """Core app."""

    name = f"{CONF.pkg_name}.apps.core"
