"""CLI entry point."""

from sys import argv, exit

from christianwhocodes import ExitCode, Text, cprint
from tawala_api.conf import PROJECT_API


def main() -> None:
    """Execute the CLI."""
    if len(argv) < 2:
        cprint("No arguments passed.", Text.ERROR)
        exit(ExitCode.ERROR)

    match argv[1]:
        case "-v" | "--version" | "version":
            from christianwhocodes import print_version

            exit(print_version(PROJECT_API.base_name))
        case _:
            from tawala_api.conf import (
                FetchProjectValidationError,
                print_invalid_project_help,
            )

            try:
                PROJECT_API.validate_project()
            except FetchProjectValidationError as e:
                exit(print_invalid_project_help(e))
            except Exception as e:
                cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
                exit(ExitCode.ERROR)
            else:
                from os import environ
                from sys import path

                from django.core.management import ManagementUtility

                from . import DJANGO_SETTINGS_MODULE

                path.insert(0, str(PROJECT_API.base_dir))
                environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
                utility = ManagementUtility(argv)
                utility.prog_name = PROJECT_API.base_name
                utility.execute()


if __name__ == "__main__":
    main()
