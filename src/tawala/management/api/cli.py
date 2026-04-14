"""CLI entry point."""

import sys

from christianwhocodes import ExitCode, Text, cprint

from ... import CONF


def main() -> None:
    """Execute the CLI."""
    if len(sys.argv) < 2:
        cprint("No arguments passed.", Text.ERROR)
        sys.exit(ExitCode.ERROR)
    match sys.argv[1]:
        case "-v" | "--ver" | "--version" | "version":
            from christianwhocodes import print_version

            sys.exit(print_version(CONF.pkg_name))

        case "startproject":
            from ..commands.startproject import main as start

            sys.exit(start(sys.argv[2:]))
        case _:
            from ... import ConfValidationError

            try:
                CONF.validate_project()
            except ConfValidationError as e:
                cprint(
                    f"Is this a valid {CONF.pkg_display_name} project directory?\n{e}",
                    Text.WARNING,
                )
                cprint(
                    f"Assuming you have uv installed:\n"
                    f"    - run: 'uvx {CONF.pkg_name} startproject <project_name>' to initialize a new project.\n"
                    f"    - run: 'uvx {CONF.pkg_name} startproject -h' to see help on the command.",
                    Text.INFO,
                )
                sys.exit(ExitCode.ERROR)
            except Exception as e:
                cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
                sys.exit(ExitCode.ERROR)
            else:
                from django.core.management import ManagementUtility

                sys.path.insert(0, str(CONF.base_dir))
                utility = ManagementUtility(sys.argv)
                utility.prog_name = CONF.pkg_name
                utility.execute()


if __name__ == "__main__":
    main()
