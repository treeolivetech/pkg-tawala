"""Package app configuration."""

from django.apps import AppConfig

from .constants import Package


class PackageConfig(AppConfig):
    """Package app configuration."""

    name = Package.NAME
