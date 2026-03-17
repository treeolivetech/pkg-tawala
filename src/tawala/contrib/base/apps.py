"""Base app configuration."""

from django.apps import AppConfig

from ...constants import Package


class BaseConfig(AppConfig):
    """Base app configuration."""

    name = f"{Package.NAME}.contrib.base"
