"""Management command for executing install operations."""

from typing import Any

from christianwhocodes import status
from django.core.management.base import BaseCommand, CommandParser

from .helpers.run import CommandGenerator, CommandOutput, FormattedCommandOutput


class _InstallCommandGenerator(CommandGenerator):
    """Generator for install command execution."""

    def get_runcommands(self) -> list[str]:
        """Retrieve install commands."""
        from ..settings import RUNCOMMANDS

        return RUNCOMMANDS.install

    def create_output_handler(self) -> CommandOutput:
        """Create the output handler for install commands."""
        from .helpers.art import ArtType

        return FormattedCommandOutput(self.dj_command, ArtType.INSTALL)

    def get_mode(self) -> str:
        """Get the mode identifier for install commands."""
        return "INSTALL"


class Command(BaseCommand):
    """Execute install commands."""

    help = "Execute install commands"

    def add_arguments(self, parser: CommandParser) -> None:
        """Define command-line arguments."""
        parser.add_argument(
            "--dry",
            "--dry-run",
            dest="dry_run",
            action="store_true",
            help="Show commands that would be executed without running them",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Run configured install commands."""
        dry_run: bool = options.get("dry_run", False)
        generator = _InstallCommandGenerator(self)
        with status("Running install commands..."):
            generator.generate(dry_run=dry_run)
