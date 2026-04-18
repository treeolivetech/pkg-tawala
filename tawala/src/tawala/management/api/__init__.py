"""Management."""

"""[FETCH_PROJECT_IMPORT_ALLOWED] Management api."""

from os import environ

from christianwhocodes import ExitCode, Text, cprint

from ..settings.fetch import FETCH_PROJECT

environ.setdefault(
    "DJANGO_SETTINGS_MODULE", f"{FETCH_PROJECT.pkg_name}.management.settings.conf"
)


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
