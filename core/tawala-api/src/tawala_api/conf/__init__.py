"""Conf."""

from christianwhocodes import ExitCode, Text, Version, cprint

from ._1_enums import *
from ._2_schema import *
from ._3_fetch import *

API_APP = "tawala_api"
API_NAME = "tawala-api"
API_VERSION = Version.get(API_NAME)[0]


def print_invalid_project_help(error: Exception) -> ExitCode:
    """Print guidance for invalid project-directory validation.

    Returns:
        ExitCode: The exit code to use after printing the guidance.

    """
    cprint(
        f"Is this a valid {PROJECT_API.base_display_name} project directory? {error}",
        Text.WARNING,
    )
    return ExitCode.ERROR
