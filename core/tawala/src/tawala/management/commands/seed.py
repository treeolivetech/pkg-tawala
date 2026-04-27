"""Management command to load multiple fixture files from a specified directory or from app fixtures directories."""

import traceback
from pathlib import Path
from typing import Any

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """Load fixture files from a directory or app fixtures paths."""

    help = (
        "Load fixture files from a specific directory, a specific app's fixtures "
        "directory, or all app fixtures directories.\n\n"
        "Usage:\n"
        f"  {settings.BASE_NAME} seed path/to/fixtures\n"
        f"  {settings.BASE_NAME} seed --app_label=myapp\n"
        f"  {settings.BASE_NAME} seed\n"
        f"  {settings.BASE_NAME} seed --verbose\n"
        f"  {settings.BASE_NAME} seed --app_label=myapp --extension=yaml\n\n"
        "Notes:\n"
        "  - Fixtures are loaded in alphabetical order\n"
        "  - The command stops on the first error\n"
        "  - Use --verbose for detailed progress output"
    )

    def add_arguments(self, parser: CommandParser) -> None:
        """Define the command line arguments."""
        parser.add_argument(
            "fixture_dir",
            type=str,
            nargs="?",
            default=None,
            help="Directory containing the fixtures",
        )
        parser.add_argument(
            "--extension",
            default="json",
            help="File extension to look for (default: json)",
        )
        parser.add_argument(
            "--app_label",
            type=str,
            help="App label to load fixtures from a specific app",
        )
        parser.add_argument(
            "--verbose", action="store_true", help="Show verbose output"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the command to load fixtures.

        The command follows this process:
        1. Determine the source of fixtures (specific dir, app dir, or all apps)
        2. Find all matching fixture files
        3. Sort files alphabetically
        4. Load each fixture in order

        If --verbose is set, provides detailed progress information.
        Stops on the first error encountered.
        """
        fixture_dir = options["fixture_dir"]
        extension = options["extension"]
        app_label = options["app_label"]
        verbose = options["verbose"]

        fixture_files: list[Path] = []

        # Case 1: Loading from a specific directory
        if fixture_dir:
            fixture_path = Path(fixture_dir).resolve()
            if not fixture_path.exists():
                self.stderr.write(
                    self.style.ERROR(f"Directory not found: {fixture_dir}")
                )
                return

            fixture_files = [
                f
                for f in fixture_path.rglob(f"*.{extension}")
                if f.name != "seed_example.json"
            ]

        # Case 2: Loading from app fixtures directories
        else:
            if app_label:
                # Load from specific app's fixtures directory
                try:
                    app_config = apps.get_app_config(app_label)
                    app_fixtures_path = Path(app_config.path) / "fixtures"
                    fixture_files = [
                        f
                        for f in app_fixtures_path.rglob(f"*.{extension}")
                        if f.name != "seed_example.json"
                    ]
                except LookupError:
                    self.stderr.write(self.style.ERROR(f"App '{app_label}' not found"))
                    return
            else:
                # Load from all apps' fixtures directories
                for app_config in apps.get_app_configs():
                    app_fixtures_path = Path(app_config.path) / "fixtures"
                    fixture_files.extend([
                        f
                        for f in app_fixtures_path.rglob(f"*.{extension}")
                        if f.name != "seed_example.json"
                    ])

        if verbose:
            self.stdout.write(f"Search pattern: *.{extension}")

        if not fixture_files:
            self.stderr.write(
                self.style.WARNING(
                    f"No .{extension} files found in {fixture_dir or 'app fixtures directories'}"
                )
            )
            return

        # Sort files to ensure consistent loading order
        fixture_files.sort()

        if verbose:
            self.stdout.write(
                self.style.SUCCESS(f"Found {len(fixture_files)} fixture files:")
            )
            for file in fixture_files:
                self.stdout.write(f"  - {file.name}")

        # Load each fixture
        for fixture_file in fixture_files:
            try:
                if verbose:
                    self.stdout.write(f"Loading fixture: {fixture_file.name}...")
                call_command("loaddata", str(fixture_file))
                if verbose:
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully loaded {fixture_file.name}")
                    )
            except Exception as e:
                error_message = "".join(
                    traceback.format_exception(None, e, e.__traceback__)
                )
                self.stderr.write(
                    self.style.ERROR(
                        f"Error loading {fixture_file.name}:\n{error_message}"
                    )
                )
                return

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully loaded all fixtures from {fixture_dir or 'app fixtures directories'}"
            )
        )
