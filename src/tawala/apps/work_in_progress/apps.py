"""Work in progress app."""

from django.apps import AppConfig

from ... import CONF


class WorkInProgressConfig(AppConfig):
    """Work in progress app."""

    name = f"{CONF.pkg_name}.apps.work_in_progress"
