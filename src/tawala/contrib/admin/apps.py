"""Admin app configuration."""

from django.apps import AppConfig

from ...constants import Package


class AdminConfig(AppConfig):
    """Admin app configuration."""

    name = f"{Package.NAME}.contrib.admin"
