"""ASCII art and terminal formatting for management commands."""

from enum import IntEnum, StrEnum
from shutil import get_terminal_size

from django.core.management.base import BaseCommand


class ArtType(StrEnum):
    """Available ASCII art types."""

    RUN = "run"
    SERVER = "server"
    BUILD = "build"
    INSTALL = "install"


class TerminalSize(IntEnum):
    """Minimum terminal width for full ASCII art."""

    THRESHOLD = 60


class ArtPrinter:
    """Prints ASCII art banners adapted to terminal width."""

    def __init__(self, command: BaseCommand) -> None:
        """Set up command reference and terminal width."""
        self.command = command
        self.terminal_width = get_terminal_size(fallback=(80, 24)).columns

    def _get_run_art(self) -> list[str]:
        """RUN ASCII art lines."""
        if self.terminal_width >= TerminalSize.THRESHOLD:
            return [
                "",
                "  ██████╗ ██╗   ██╗███╗   ██╗",
                "  ██╔══██╗██║   ██║████╗  ██║",
                "  ██████╔╝██║   ██║██╔██╗ ██║",
                "  ██╔══██╗██║   ██║██║╚██╗██║",
                "  ██║  ██║╚██████╔╝██║ ╚████║",
                "  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝",
                "",
            ]
        else:
            return ["", "  █▀█ █░█ █▄░█", "  █▀▄ █▄█ █░▀█", ""]

    def _get_server_art(self) -> list[str]:
        """SERVER ASCII art lines."""
        run_art = self._get_run_art()

        if self.terminal_width >= TerminalSize.THRESHOLD:
            server_art = [
                "   ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ ",
                "   ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗",
                "   ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝",
                "   ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗",
                "   ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║",
                "   ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝",
                "",
            ]
        else:
            server_art = ["  █▀ █▀▀ █▀█ █░█ █▀▀ █▀█", "  ▄█ ██▄ █▀▄ ▀▄▀ ██▄ █▀▄", ""]

        return run_art + server_art

    def _get_build_art(self) -> list[str]:
        """BUILD ASCII art lines."""
        run_art = self._get_run_art()

        if self.terminal_width >= TerminalSize.THRESHOLD:
            build_art = [
                "        ██████╗ ██╗   ██╗██╗██╗     ██████╗ ",
                "        ██╔══██╗██║   ██║██║██║     ██╔══██╗",
                "        ██████╔╝██║   ██║██║██║     ██║  ██║",
                "        ██╔══██╗██║   ██║██║██║     ██║  ██║",
                "        ██████╔╝╚██████╔╝██║███████╗██████╔╝",
                "        ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝ ",
                "",
            ]
        else:
            build_art = ["       █▄▄ █░█ █ █░░ █▀▄", "       █▄█ █▄█ █ █▄▄ █▄▀", ""]

        return run_art + build_art

    def _get_install_art(self) -> list[str]:
        """INSTALL ASCII art lines."""
        run_art = self._get_run_art()

        if self.terminal_width >= TerminalSize.THRESHOLD:
            install_art = [
                "   ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ",
                "   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ",
                "   ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     ",
                "   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ",
                "   ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗",
                "   ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝",
                "",
            ]
        else:
            install_art = [
                "    █ █▄░█ █▀ ▀█▀ ▄▀█ █░░ █░░",
                "    █ █░▀█ ▄█ ░█░ █▀█ █▄▄ █▄▄",
                "",
            ]

        return run_art + install_art

    def _get_art(self, art_type: ArtType) -> list[str]:
        """Get ASCII art lines for the given type."""
        art_getters = {
            ArtType.RUN: self._get_run_art,
            ArtType.SERVER: self._get_server_art,
            ArtType.BUILD: self._get_build_art,
            ArtType.INSTALL: self._get_install_art,
        }

        getter = art_getters.get(art_type)
        if getter is None:
            raise ValueError(f"Unknown art type: {art_type}")

        return getter()

    def _print_banner(
        self,
        art_type: ArtType,
        title: str,
        subtitle: str | None = None,
        notice: str | None = None,
    ) -> None:
        """Print an ASCII art banner with optional subtitle and notice."""
        art_lines = self._get_art(art_type)

        # Print ASCII art
        for line in art_lines:
            self.command.stdout.write(self.command.style.HTTP_INFO(line))

        # Print title
        self.command.stdout.write(self.command.style.HTTP_INFO(title))

        # Print subtitle if provided
        if subtitle:
            self.command.stdout.write(self.command.style.WARNING(subtitle))

        # Print notice if provided
        if notice:
            self.command.stdout.write(self.command.style.NOTICE(notice))

        self.command.stdout.write("")

    def print_dev_server_banner(self) -> None:
        """Print the development server banner."""
        if self.terminal_width >= TerminalSize.THRESHOLD:
            self._print_banner(
                art_type=ArtType.SERVER,
                title="         🔥  Development Server  🔥",
                subtitle="       ⚠️  Not suitable for production!  ⚠️",
                notice="             Press Ctrl-C to quit",
            )
        else:
            self._print_banner(
                art_type=ArtType.SERVER,
                title="    🔥  Dev Server  🔥",
                subtitle="  ⚠️   Not for production! ⚠️",
                notice="       Ctrl-C to quit",
            )

    def print_run_process_banner(
        self, art_type: ArtType, display_mode: str, command_count: int
    ) -> None:
        """Print a banner for build/install command processes."""
        if self.terminal_width >= TerminalSize.THRESHOLD:
            self._print_banner(
                art_type=art_type,
                title=f"              🔨  {display_mode} Process  🔨",
                notice=f"           {command_count} command(s) to execute",
            )
        else:
            self._print_banner(
                art_type=art_type,
                title=f"      🔨  {display_mode}  🔨",
                notice=f"    {command_count} command(s)",
            )
