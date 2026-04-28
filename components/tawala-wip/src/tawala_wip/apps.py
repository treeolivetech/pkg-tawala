"""WIP Configuration."""

from christianwhocodes import Version
from django.apps import AppConfig

WIP_APP = "tawala_wip"
WIP_NAME = "tawala-wip"
WIP_VERSION = Version.get(WIP_NAME)[0]


class WIPConfig(AppConfig):
    """WIP app."""

    name = WIP_APP
