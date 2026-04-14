"""[BASE_CONF_IMPORT_ALLOWED_PREINIT] CLI entry point."""

from sys import argv, exit, path

from christianwhocodes import ExitCode, Text, cprint

from ...settings.conf import BASE_CONF


def main() -> None:
    """Execute the CLI."""
    if len(argv) < 2:
        cprint("No arguments passed.", Text.ERROR)
        exit(ExitCode.ERROR)

    match argv[1]:
        case "-v" | "--ver" | "--version" | "version":
            from christianwhocodes import print_version

            exit(print_version(BASE_CONF.pkg_name))
        case _:
            from ...settings.conf import BaseValidationError

            try:
                BASE_CONF.validate_project()
            except BaseValidationError as e:
                cprint(
                    f"Is this a valid {BASE_CONF.pkg_display_name} project directory?\n{e}",
                    Text.WARNING,
                )
                cprint(
                    f"Assuming you have uv installed:\n"
                    f"    - run: 'uvx {BASE_CONF.create_pkg_name} <project_name>' to initialize a new project.\n"
                    f"    - run: 'uvx {BASE_CONF.create_pkg_name} -h' to see help on the command.",
                    Text.INFO,
                )
                exit(ExitCode.ERROR)
            except Exception as e:
                cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
                exit(ExitCode.ERROR)
            else:
                from django.core.management import ManagementUtility

                path.insert(0, str(BASE_CONF.base_dir))
                utility = ManagementUtility(argv)
                utility.prog_name = BASE_CONF.pkg_name
                utility.execute()


if __name__ == "__main__":
    main()
