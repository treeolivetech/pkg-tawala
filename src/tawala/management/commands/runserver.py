"""Custom runserver."""

from typing import Any

from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand
from django.core.management.base import CommandParser

from ...constants import Package


class Command(RunserverCommand):
    """Development server."""

    help = f"{Package.NAME} Development server"

    # Django's runserver sets these at runtime; declared here for type checking
    _raw_ipv6: bool
    addr: str
    port: str
    protocol: str
    use_ipv6: bool

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the runserver command."""
        super().__init__(*args, **kwargs)
        self.no_clipboard: bool = False

    def add_arguments(self, parser: CommandParser) -> None:
        """Add custom arguments to the command."""
        super().add_arguments(parser)
        parser.add_argument("--no-clipboard", action="store_true", help="Disable copying the server URL to clipboard")

    def handle(self, *args: object, **options: Any) -> str | None:
        """Handle the dev command execution."""
        self.no_clipboard = options.get("no_clipboard", False)
        return super().handle(*args, **options)

    def check_migrations(self) -> None:
        """Warn about unapplied migrations."""
        from django.core.exceptions import ImproperlyConfigured
        from django.db import DEFAULT_DB_ALIAS, connections
        from django.db.migrations.executor import MigrationExecutor

        try:
            executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
        except ImproperlyConfigured:
            return

        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if not plan:
            return

        apps_waiting_migration = sorted({migration.app_label for migration, _ in plan})
        self.stdout.write(
            self.style.NOTICE(
                f"\nYou have {len(plan)} unapplied migration(s). "
                f"Your project may not work properly until you apply the "
                f"migrations for app(s): {', '.join(apps_waiting_migration)}."
            )
        )
        self.stdout.write(self.style.NOTICE(f"Run {Package.NAME} migrate to apply them."))

    def on_bind(self, server_port: int) -> None:
        """Display startup banner and server info."""
        self._print_startup_banner()
        self._print_server_info(server_port)

        if not self.no_clipboard:
            self._copy_to_clipboard(server_port)

        self.stdout.write("")

    # ========== Display Methods ==========

    def _print_startup_banner(self) -> None:
        """Print ASCII banner."""
        from .helpers.art import ArtPrinter

        ArtPrinter(self).print_dev_server_banner()

    def _print_server_info(self, server_port: int) -> None:
        """Print timestamp, version, and URL info."""
        self._print_timestamp()
        self._print_version()
        self._print_local_url(server_port)

        if self.addr in ("0", "0.0.0.0"):
            self._print_network_url(server_port)

    def _print_timestamp(self) -> None:
        """Print current date/time with timezone."""
        from django.utils import timezone

        tz = timezone.get_current_timezone()
        now = timezone.localtime(timezone.now(), timezone=tz)
        timestamp = now.strftime("%B %d, %Y - %X")
        tz_name = now.strftime("%Z")

        date_display = f"\n  📅 Date: {self.style.HTTP_NOT_MODIFIED(timestamp)}"
        if tz_name:
            date_display += f" ({tz_name})"

        self.stdout.write(date_display)

    def _print_version(self) -> None:
        """Print version."""
        self.stdout.write(f"  🔧 {Package.DISPLAY_NAME} version: {self.style.HTTP_NOT_MODIFIED(Package.VERSION)}")

    def _print_local_url(self, server_port: int) -> None:
        """Print local server URL."""
        url = f"{self.protocol}://{self._format_address()}:{server_port}/"
        self.stdout.write(f"  🌐 Local address:   {self.style.SUCCESS(url)}")

    def _print_network_url(self, server_port: int) -> None:
        """Print LAN IP address if available."""
        from socket import gaierror, gethostbyname, gethostname

        try:
            hostname = gethostname()
            local_ip = gethostbyname(hostname)
            network_url = f"{self.protocol}://{local_ip}:{server_port}/"
            self.stdout.write(f"  🌍 Network address: {self.style.SUCCESS(network_url)}")
        except gaierror:
            pass

    def _copy_to_clipboard(self, server_port: int) -> None:
        """Copy server URL to clipboard."""
        try:
            from pyperclip import copy

            url = f"{self.protocol}://{self._format_address()}:{server_port}/"
            copy(url)
            self.stdout.write(f"  📋 {self.style.SUCCESS('Copied to clipboard!')}")
        except ImportError:
            self.stdout.write(f"  📋 {self.style.WARNING('pyperclip not installed - skipping clipboard copy')}")
        except Exception:
            pass

    def _format_address(self) -> str:
        """Format address for display."""
        if self._raw_ipv6:
            return f"[{self.addr}]"
        return "0.0.0.0" if self.addr == "0" else self.addr
