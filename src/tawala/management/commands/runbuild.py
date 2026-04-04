"""Management command for executing build operations."""

from typing import Any

from christianwhocodes import status
from django.core.management.base import BaseCommand, CommandParser

from .helpers.run import CommandGenerator, CommandOutput, FormattedCommandOutput


class _BuildCommandGenerator(CommandGenerator):
    """Generator for build command execution."""

    def get_runcommands(self) -> list[str]:
        """Retrieve build commands."""
        from ..settings import RUNCOMMANDS

        return RUNCOMMANDS.build

    def create_output_handler(self) -> CommandOutput:
        """Create the output handler for build commands."""
        from .helpers.art import ArtType

        return FormattedCommandOutput(self.dj_command, ArtType.BUILD)

    def get_mode(self) -> str:
        """Get the mode identifier for build commands."""
        return "BUILD"


class Command(BaseCommand):
    """Execute build commands."""

    help = "Execute build commands"

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
        """Run configured build commands."""
        dry_run: bool = options.get("dry_run", False)
        generator = _BuildCommandGenerator(self)
        with status("Running build commands..."):
            generator.generate(dry_run=dry_run)
