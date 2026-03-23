"""Package app configuration."""

from django.apps import AppConfig

from . import Package


class PackageConfig(AppConfig):
    """Package app configuration."""

    name = Package.NAME
