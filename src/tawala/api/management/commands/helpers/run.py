"""Shared utilities for install and build command execution."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from .art import ArtPrinter, ArtType


@dataclass
class CommandResult:
    """Result of a single command execution."""

    command: str
    success: bool
    error: str | None = None


class CommandOutput(ABC):
    """Interface for command process output display."""

    def __init__(self, command: BaseCommand) -> None:
        """Store the management command reference."""
        self.command = command

    @abstractmethod
    def print_header(self, command_count: int, dry_run: bool, mode: str) -> None:
        """Print the process header."""
        pass

    @abstractmethod
    def print_no_commands_error(self, mode: str) -> None:
        """Print error when no commands are configured."""
        pass

    @abstractmethod
    def print_dry_run_preview(self, commands: list[str]) -> None:
        """Print a preview of commands without executing."""
        pass

    @abstractmethod
    def print_command_header(self) -> None:
        """Print separator before each command."""
        pass

    @abstractmethod
    def print_command_success(self, cmd: str, index: int, total: int) -> None:
        """Print successful command completion."""
        pass

    @abstractmethod
    def print_command_failure(self, cmd: str, error: str, index: int, total: int) -> None:
        """Print command failure info."""
        pass

    @abstractmethod
    def print_summary(self, total: int, completed: int, failed: int) -> None:
        """Print the final summary."""
        pass


class CommandExecutor:
    """Executes individual management commands with error handling."""

    def __init__(self, command: BaseCommand) -> None:
        """Store the management command reference."""
        self.command = command

    def execute(self, cmd: str) -> CommandResult:
        """Parse and execute a single management command string."""
        try:
            # Validate and parse command
            parts: list[str] = cmd.strip().split()
            if not parts:
                return CommandResult(command=cmd, success=False, error="Empty command string")

            command_name: str = parts[0]
            command_args: list[str] = parts[1:]

            # Execute the management command
            call_command(command_name, *command_args)

            return CommandResult(command=cmd, success=True)
        except CommandError as e:
            return CommandResult(command=cmd, success=False, error=str(e))
        except (ValueError, OSError) as e:
            return CommandResult(command=cmd, success=False, error=str(e))


class CommandProcess:
    """Orchestrates command execution with output and progress tracking."""

    def __init__(self, command: BaseCommand, output: CommandOutput, executor: CommandExecutor, mode: str) -> None:
        """Set up command, output handler, executor, and mode."""
        self.command = command
        self.output = output
        self.executor = executor
        self.mode = mode

    def run(self, commands: list[str], dry_run: bool = False) -> None:
        """Run commands or preview them in dry-run mode."""
        self.output.print_header(len(commands), dry_run, self.mode)

        if dry_run:
            self.output.print_dry_run_preview(commands)
            return

        self._execute_commands(commands)

    def _execute_commands(self, commands: list[str]) -> None:
        """Execute all commands sequentially."""
        total = len(commands)
        completed = 0
        failed = 0
        results: list[CommandResult] = []

        for i, cmd in enumerate(commands, 1):
            self.output.print_command_header()
            result = self.executor.execute(cmd)
            results.append(result)

            if result.success:
                self.output.print_command_success(cmd, i, total)
                completed += 1
            else:
                self.output.print_command_failure(cmd, result.error or "Unknown error", i, total)
                failed += 1

        self.output.print_summary(total, completed, failed)


class CommandGenerator(ABC):
    """Base class for building command execution processes."""

    def __init__(self, dj_command: BaseCommand) -> None:
        """Store the Django management command reference."""
        self.dj_command = dj_command

    @abstractmethod
    def get_runcommands(self) -> list[str]:
        """Retrieve the list of commands to execute."""
        pass

    @abstractmethod
    def create_output_handler(self) -> CommandOutput:
        """Create the output handler."""
        pass

    @abstractmethod
    def get_mode(self) -> str:
        """Return the mode identifier (e.g., 'BUILD', 'INSTALL')."""
        pass

    def generate(self, dry_run: bool = False) -> None:
        """Build and execute the command process."""
        commands = self.get_runcommands()

        if not commands:
            output = self.create_output_handler()
            output.print_no_commands_error(self.get_mode().lower())
            return

        # Initialize components
        output = self.create_output_handler()
        executor = CommandExecutor(self.dj_command)
        process = CommandProcess(self.dj_command, output, executor, self.get_mode())

        # Run the process
        process.run(commands, dry_run=dry_run)


class FormattedCommandOutput(CommandOutput):
    """Colorful output with ASCII art, progress bars, and emojis."""

    def __init__(self, command: BaseCommand, art_type: ArtType) -> None:
        """Set up command reference and art type."""
        super().__init__(command)
        self.art_type = art_type
        self.art_printer = ArtPrinter(command)

    def print_header(self, command_count: int, dry_run: bool, mode: str) -> None:
        """Print header with ASCII art."""
        display_mode = "DRY RUN" if dry_run else mode

        self.command.stdout.write(self.command.style.SUCCESS(f"\n✨ Starting {display_mode.lower()} process...\n"))

        self.art_printer.print_run_process_banner(self.art_type, display_mode, command_count)

    def print_no_commands_error(self, mode: str) -> None:
        """Print error when no commands configured."""
        self.command.stdout.write(self.command.style.ERROR(f"\n❌ No {mode} commands configured!"))
        self.command.stdout.write("")

    def print_dry_run_preview(self, commands: list[str]) -> None:
        """Print numbered command list preview."""
        self.command.stdout.write(self.command.style.NOTICE("Commands to be executed:\n"))

        for i, cmd in enumerate(commands, 1):
            self.command.stdout.write(f"  {self.command.style.NOTICE(f'[{i}]')} {self.command.style.HTTP_INFO(cmd)}")

        self.command.stdout.write("")
        self.command.stdout.write(self.command.style.HTTP_NOT_MODIFIED("✨ Remove --dry-run flag to execute these commands"))
        self.command.stdout.write("")

    def print_command_header(self) -> None:
        """Print the command header before execution."""
        self.command.stdout.write(self.command.style.HTTP_NOT_MODIFIED("=" * 60 + "\n"))

    def print_command_success(self, cmd: str, index: int, total: int) -> None:
        """Print success with progress bar."""
        progress_bar = self._create_progress_bar(index, total)
        self.command.stdout.write(f"\n{progress_bar}")
        self.command.stdout.write(self.command.style.SUCCESS(f"✓ Completed: {cmd}"))
        self.command.stdout.write("")

    def print_command_failure(self, cmd: str, error: str, index: int, total: int) -> None:
        """Print failure with progress bar."""
        progress_bar = self._create_progress_bar(index, total)
        self.command.stdout.write(f"\n{progress_bar}")
        self.command.stdout.write(self.command.style.ERROR(f"✗ Failed: {cmd}"))
        self.command.stdout.write(self.command.style.ERROR(f"   Error: {error}"))
        self.command.stdout.write("")

    def print_summary(self, total: int, completed: int, failed: int) -> None:
        """Print final completion summary."""
        self.command.stdout.write(self.command.style.HTTP_NOT_MODIFIED("=" * 60 + "\n"))
        if failed == 0:
            self.command.stdout.write(self.command.style.SUCCESS(f"🎉 All {completed} command(s) completed successfully!"))
        else:
            self.command.stdout.write(self.command.style.SUCCESS(f"✓ {completed}/{total} command(s) completed"))
            self.command.stdout.write(self.command.style.ERROR(f"✗ {failed}/{total} command(s) failed"))

        self.command.stdout.write("")

    def _create_progress_bar(self, current: int, total: int) -> str:
        """Create a visual progress bar string."""
        bar_length = 40
        filled = int(bar_length * current / total)
        bar = "█" * filled + "░" * (bar_length - filled)
        percentage = (current / total) * 100

        return (
            f"  [{bar}] {self.command.style.HTTP_INFO(f'{current}/{total}')} ({self.command.style.NOTICE(f'{percentage:.0f}%')})"
        )
