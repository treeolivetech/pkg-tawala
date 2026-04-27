"""CLI Entry point."""

from argparse import ArgumentParser, Namespace
from sys import argv, exit
from typing import Callable, NoReturn, cast

from christianwhocodes import ExitCode


def _build_parser() -> ArgumentParser:
    """Create and configure the top-level CLI parser."""
    from .commands import GenerateCommand, NewCommand
    from .conf import API_NAME, API_VERSION

    parser = ArgumentParser(
        prog=API_NAME,
        description=f"{API_NAME} CLI.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=API_VERSION,
        help="Show package version and exit.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # new
    new_command = NewCommand()
    new_parser = subparsers.add_parser(
        "new",
        help=new_command.help,
        description=new_command.help,
    )
    new_command.add_arguments(new_parser)
    new_parser.set_defaults(command_handler=new_command.handle)

    # generate
    generate_command = GenerateCommand()
    generate_parser = subparsers.add_parser(
        "generate",
        help=generate_command.help,
        description=generate_command.help,
    )
    generate_command.add_arguments(generate_parser)
    generate_parser.set_defaults(command_handler=generate_command.handle)

    return parser


def _handle_args(args: Namespace, parser: ArgumentParser) -> int | ExitCode:
    """Execute the command represented by parsed arguments."""
    command_handler = cast(
        Callable[[Namespace], int | ExitCode] | None,
        getattr(args, "command_handler", None),
    )
    if callable(command_handler):
        return command_handler(args)

    parser.print_help()

    return ExitCode.ERROR


def main() -> NoReturn:
    """Execute the project initialization command."""
    parser = _build_parser()
    parsed_args = parser.parse_args(argv[1:])
    exit(_handle_args(parsed_args, parser))


if __name__ == "__main__":
    main()
