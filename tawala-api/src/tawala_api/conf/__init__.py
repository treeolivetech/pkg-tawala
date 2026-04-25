"""Conf."""

from christianwhocodes import ExitCode, Text, Version, cprint

from .enums import *
from .fetch import *
from .mappings import *

API_PKG_NAME = "tawala-api"
API_PKG_MODULE = "tawala_api"
API_PKG_VERSION = Version.get(API_PKG_NAME)[0]

DJANGO_SETTINGS_MODULE = f"{FETCH_PROJECT.core_app}.management.conf"


def print_invalid_project_help(error: Exception) -> ExitCode:
    """Print guidance for invalid project-directory validation.

    Returns:
        ExitCode: The exit code to use after printing the guidance.

    """
    cprint(
        f"Is this a valid {FETCH_PROJECT.pkg_display_name} project directory? {error}",
        Text.WARNING,
    )
    return ExitCode.ERROR
