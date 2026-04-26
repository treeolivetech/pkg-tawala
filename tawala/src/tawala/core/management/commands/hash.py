"""Generate a hashed password for use in fixtures."""

from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """Generate a hashed password for use in fixtures."""

    help = "Generate a hashed password for use in fixtures."

    def add_arguments(self, parser: CommandParser) -> None:
        """Define the command line arguments."""
        parser.add_argument(
            "password", type=str, help="The plain text password to hash"
        )

    def handle(self, *args: Any, **options: Any):
        """Handle."""
        password = options["password"]
        hashed_password = make_password(password)
        self.stdout.write(self.style.SUCCESS(f"Hashed password: {hashed_password}"))
