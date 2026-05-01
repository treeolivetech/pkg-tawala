"""School app."""

from christianwhocodes import Version
from django.apps import AppConfig

SCHOOL_APP = "tawala_school"
SCHOOL_NAME = "tawala-school"
SCHOOL_VERSION = Version.get(SCHOOL_NAME)[0]


class SchoolConfig(AppConfig):
    """School app."""

    name = SCHOOL_APP
