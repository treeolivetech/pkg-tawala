"""CLI entry point."""

from sys import argv, exit

from christianwhocodes import ExitCode, Text, cprint
from treeolive_api.conf import FETCH_PROJECT


def main() -> None:
    """Execute the CLI."""
    if len(argv) < 2:
        cprint("No arguments passed.", Text.ERROR)
        exit(ExitCode.ERROR)

    match argv[1]:
        case "-v" | "--version" | "version":
            from christianwhocodes import print_version

            exit(print_version(FETCH_PROJECT.core_name))
        case _:
            from treeolive_api.conf import (
                DJANGO_SETTINGS_MODULE,
                FetchProjectValidationError,
                print_invalid_project_help,
            )

            try:
                FETCH_PROJECT.validate_project()
            except FetchProjectValidationError as e:
                exit(print_invalid_project_help(e))
            except Exception as e:
                cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
                exit(ExitCode.ERROR)
            else:
                from os import environ
                from sys import path

                from django.core.management import ManagementUtility

                path.insert(0, str(FETCH_PROJECT.base_dir))
                environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
                utility = ManagementUtility(argv)
                utility.prog_name = FETCH_PROJECT.core_name
                utility.execute()


if __name__ == "__main__":
    main()
