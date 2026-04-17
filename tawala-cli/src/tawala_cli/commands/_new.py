"""`new` command/script."""

from argparse import ArgumentParser, Namespace
from pathlib import Path
from subprocess import CalledProcessError, run
from sys import executable

from christianwhocodes import (
    BaseCommand,
    ExitCode,
    PostgresFilename,
    Text,
    Version,
    cprint,
    status,
)

from tawala import (
    PROJECT_CONF,
    DatabaseKeys,
    DatabaseOptions,
    LayoutKeys,
    LayoutOptions,
    PresetKeys,
    PresetOptions,
)

__all__ = ["NewCommand"]


class NewCommand(BaseCommand):
    """Command to initialize a new project."""

    _project_dir: Path
    _validated_args: Namespace
    _project_dir_existed_before: bool
    prog = PROJECT_CONF.cli_pkg_name
    help = f"Initialize a new {PROJECT_CONF.pkg_display_name} app."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser."""
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=Version.get(PROJECT_CONF.cli_pkg_name)[0],
            help="Show package version and exit.",
        )

        parser.add_argument(
            "project_name",
            help=(
                "Name of the project to initialize. Can also be '.' to initialize in the current directory."
            ),
        )

        parser.add_argument(
            f"--{PresetKeys.PRESET}",
            choices=list(PresetOptions),
            default=PresetOptions.DEFAULT,
            help=f"Preset to use. Defaults to the '{PresetOptions.DEFAULT}' preset.",
        )

        parser.add_argument(
            f"--{DatabaseKeys.DB}",
            choices=list(DatabaseOptions),
            help=(
                "Database backend to use. Defaults to SQLite if not specified. "
                f"Note: the {PresetOptions.VERCEL} preset automatically uses {DatabaseOptions.POSTGRESQL}. "
                "Other presets work with either database backend, "
                "so choose based on your needs and preferences. "
                f"Defaults to {DatabaseOptions.DEFAULT_SQLITE} if not specified."
            ),
        )

        parser.add_argument(
            f"--{DatabaseKeys.USE_VARS_OPTION}",
            action="store_true",
            help=(
                "Use environment / pyproject.toml variables for PostgreSQL configuration. "
                "If False, configuration will be read from "
                f"{PostgresFilename.PGSERVICE} and {PostgresFilename.PGPASS} files. "
                "Note: this flag is only applicable if the database backend is set to "
                f"{DatabaseOptions.POSTGRESQL}. "
                f"The {PresetOptions.VERCEL} preset automatically sets this flag to True "
                "since Vercel requires environment variable configuration for PostgreSQL "
                "and does not support file-based configuration."
            ),
        )

        parser.add_argument(
            f"--{LayoutKeys.LAYOUT}",
            choices=list(LayoutOptions),
            help=f"Layout to use for the generated project. Defaults to the standard {LayoutOptions.DEFAULT_BASE} layout if not specified.",
        )

    def handle(self, args: Namespace) -> ExitCode:
        """Execute the command logic with the parsed arguments."""
        try:
            self._project_dir = Path.cwd() / args.project_name
            self._project_dir_existed_before = self._project_dir.exists()
            self._validated_args = self._validate_args(args)
            self._validate_project_directory(self._project_dir, self._validated_args)
            with status("Generating project files..."):
                self._generate_project_files(self._project_dir, self._validated_args)
        except Exception as e:
            cprint(
                f"Something went wrong during project initialization:\n{e}",
                Text.WARNING,
            )
            self._revert_generated_files(self._project_dir)
            return ExitCode.ERROR
        else:
            self._display_successful_setup_info(self._project_dir)
            return ExitCode.SUCCESS

    def _validate_args(self, args: Namespace) -> Namespace:
        match getattr(args, PresetKeys.PRESET):
            case PresetOptions.VERCEL:
                # Enforce postgresql and environment variable configuration for Vercel preset
                # due to platform requirements and security best practices.
                if getattr(args, DatabaseKeys.DB) == DatabaseOptions.DEFAULT_SQLITE:
                    raise ValueError(
                        f"The {PresetOptions.VERCEL} preset requires {DatabaseOptions.POSTGRESQL}."
                    )
                setattr(args, DatabaseKeys.DB, DatabaseOptions.POSTGRESQL)
                setattr(args, DatabaseKeys.USE_VARS_OPTION, True)
            case _:
                # Other presets work with either database.
                # Default to sqlite if getattr(args, DatabaseKeys.DB) is unspecified.
                if not getattr(args, DatabaseKeys.DB):
                    setattr(
                        args,
                        DatabaseKeys.DB,
                        DatabaseOptions.DEFAULT_SQLITE,
                    )

        if (
            getattr(args, DatabaseKeys.USE_VARS_OPTION)
            and not getattr(args, DatabaseKeys.DB) == DatabaseOptions.POSTGRESQL
        ):
            raise ValueError(
                f"The --{DatabaseKeys.USE_VARS_OPTION} flag is only supported for {DatabaseOptions.POSTGRESQL}."
            )

        return args

    def _validate_project_directory(self, project_dir: Path, args: Namespace) -> None:
        """Ensure destination directory is safe to initialize."""
        if args.project_name == "." and any(project_dir.iterdir()):
            raise FileExistsError(
                "The current directory is not empty. "
                "Please choose a different project name or remove the existing files."
            )
        if not project_dir.exists():
            return
        if project_dir.is_file():
            raise FileExistsError(
                f"A file named '{project_dir}' already exists. "
                "Please choose a different project name or remove the existing file."
            )
        if any(project_dir.iterdir()):
            raise FileExistsError(
                f"The directory '{project_dir}' already exists and is not empty. "
                "Please choose a different project name or remove the existing files "
                "in the directory."
            )

    def _generate_project_files(self, project_dir: Path, args: Namespace) -> None:
        """Generate project scaffold by delegating to the CLI generate command."""
        self._run_generate_subprocess(
            target="all",
            project_dir=project_dir,
            args=args,
        )

    def _run_generate_subprocess(
        self,
        target: str,
        project_dir: Path,
        args: Namespace,
    ) -> None:
        """Invoke the generate subcommand in a subprocess for decoupled scaffolding."""
        command = [
            executable,
            "-m",
            "tawala_cli.cli",
            "generate",
            target,
            "--output-dir",
            str(project_dir),
            "--project-name",
            project_dir.name,
            f"--{PresetKeys.PRESET}",
            str(getattr(args, PresetKeys.PRESET)),
            f"--{DatabaseKeys.DB}",
            str(getattr(args, DatabaseKeys.DB)),
        ]

        layout = getattr(args, LayoutKeys.LAYOUT)
        if layout:
            command.extend([f"--{LayoutKeys.LAYOUT}", str(layout)])

        if getattr(args, DatabaseKeys.USE_VARS_OPTION):
            command.append(f"--{DatabaseKeys.USE_VARS_OPTION}")

        try:
            run(command, check=True, capture_output=True, text=True)
        except CalledProcessError as e:
            stderr = (e.stderr or "").strip()
            stdout = (e.stdout or "").strip()
            details = stderr or stdout or str(e)
            raise RuntimeError(
                f"Generate command failed for target '{target}': {details}"
            ) from e

    def _revert_generated_files(self, project_dir: Path) -> None:
        """Delete generated files only when the target directory was newly created."""
        # Never clean up pre-existing directories to avoid deleting user files
        # (especially when the user attempted initialization in '.').
        if self._project_dir_existed_before:
            return

        if project_dir.exists() and project_dir.is_dir() and any(project_dir.iterdir()):
            for item in sorted(project_dir.rglob("*"), reverse=True):
                item.unlink() if item.is_file() else item.rmdir()

    def _display_successful_setup_info(self, project_dir: Path) -> None:
        """Print success output after initialization."""
        cprint(
            f"✓ {PROJECT_CONF.pkg_display_name} project '{project_dir.name}' initialized successfully!",
            Text.SUCCESS,
        )
