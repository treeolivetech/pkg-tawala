"""CLI entry point."""

import sys

from christianwhocodes import ExitCode, InitAction, Text, cprint

from ..constants import Package, Project


def main() -> None:
    """Execute the CLI."""
    if len(sys.argv) < 2:
        cprint("No arguments passed.", Text.ERROR)
        sys.exit(ExitCode.ERROR)
    match sys.argv[1]:
        case "-v" | "--version" | "version":
            from christianwhocodes import print_version

            sys.exit(print_version(Package.NAME))
        case command if command in InitAction:
            from .commands.startproject import Command

            sys.exit(Command()(sys.argv[2:]))
        case _:
            from .conf import PROJECT_CONF, ProjectValidationError

            try:
                PROJECT_CONF.validate()
            except ProjectValidationError as e:
                cprint(f"Is this a valid {Package.DISPLAY_NAME} project directory?\n{e}", Text.WARNING)
                cprint(
                    f"Assuming you have uv installed:\n"
                    f"    - run: 'uvx {Package.NAME} {InitAction.STARTPROJECT} <project_name>' to initialize a new project.\n"
                    f"    - run: 'uvx {Package.NAME} {InitAction.STARTPROJECT} -h' to see help on the command.",
                    Text.INFO,
                )
                sys.exit(ExitCode.ERROR)
            except Exception as e:
                cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
                sys.exit(ExitCode.ERROR)
            else:
                from os import environ

                from django.core.management import ManagementUtility

                sys.path.insert(0, str(Project.BASE_DIR))
                environ.setdefault("DJANGO_SETTINGS_MODULE", Package.SETTINGS_MODULE)
                utility = ManagementUtility(sys.argv)
                utility.prog_name = Package.NAME
                utility.execute()


if __name__ == "__main__":
    main()
