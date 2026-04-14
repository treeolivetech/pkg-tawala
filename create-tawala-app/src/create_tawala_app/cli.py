"""CLI Entry point."""

from sys import argv, exit
from typing import NoReturn

from christianwhocodes import ExitCode


def main() -> NoReturn:
    """Execute the project initialization command."""
    if len(argv) < 2:
        print("No arguments passed.")
        exit(ExitCode.ERROR)

    match argv[1]:
        case "-v" | "--ver" | "--version" | "version":
            from christianwhocodes import print_version
            from tawala import BASE_CONF

            exit(print_version(BASE_CONF.create_pkg_name))
        case _:
            from .scripts import StartProject

            exit(StartProject()(argv[1:]))


if __name__ == "__main__":
    main()
