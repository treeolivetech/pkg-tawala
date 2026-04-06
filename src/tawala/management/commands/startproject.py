"""initialization command."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from christianwhocodes import (
    BaseCommand,
    ExitCode,
    FileGenerator,
    FileSpec,
    InitAction,
    PostgresFilename,
    Text,
    cprint,
    status,
)

from ... import Package
from ..enums import (
    DatabaseBackendOptions,
    DatabaseFlags,
    DatabaseTomlKeys,
    InternationalizationTomlKeys,
    MainAppFlags,
    MainAppOptions,
    MainAppTomlKeys,
    PresetFlags,
    PresetOptions,
    SecurityTomlKeys,
    StorageBackendOptions,
    StorageTomlKeys,
)


class Command(BaseCommand):
    """Command to initialize a new project."""

    _project_dir: Path
    _validated_args: Namespace
    _actions = " | ".join(InitAction)
    prog = f"{Package.NAME} [{_actions}] <project_name>"
    help = f"Initialize a new {Package.DISPLAY_NAME} project."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser."""
        parser.add_argument(
            "project_name",
            help=("Name of the project to initialize. Can also be '.' to initialize in the current directory."),
        )

        parser.add_argument(
            PresetFlags.PRESET,
            choices=[p for p in PresetOptions],
            default=PresetOptions.DEFAULT,
            help=f"Preset to use. Defaults to the '{PresetOptions.DEFAULT}' preset.",
        )

        parser.add_argument(
            DatabaseFlags.DB,
            choices=[db for db in DatabaseBackendOptions],
            help=(
                "Database backend to use. Defaults to SQLite if not specified. "
                f"Note: the {PresetOptions.VERCEL} preset automatically uses {DatabaseBackendOptions.POSTGRESQL}. "
                "Other presets work with either database backend, "
                "so choose based on your needs and preferences. "
                f"Defaults to {DatabaseBackendOptions.SQLITE} if not specified."
            ),
        )

        parser.add_argument(
            DatabaseFlags.USE_VARS,
            action="store_true",
            help=(
                "Use environment / pyproject.toml variables for PostgreSQL configuration. "
                "If False, configuration will be read from "
                f"{PostgresFilename.PGSERVICE} and {PostgresFilename.PGPASS} files. "
                "Note: this flag is only applicable if the database backend is set to "
                f"{DatabaseBackendOptions.POSTGRESQL}. "
                f"The {PresetOptions.VERCEL} preset automatically sets this flag to True "
                "since Vercel requires environment variable configuration for PostgreSQL "
                "and does not support file-based configuration."
            ),
        )

        parser.add_argument(
            "--wip",
            "--work-in-progress",
            dest="wip",
            action="store_true",
            help="Initialize the project in Work-In-Progress mode.",
        )

        parser.add_argument(
            MainAppFlags.APP,
            default=MainAppOptions.HOME,
            help=f"Name of the main app. Defaults to '{MainAppOptions.HOME}'.",
        )

    def handle(self, args: Namespace) -> ExitCode:
        """Execute the command logic with the parsed arguments."""
        try:
            self._project_dir = Path.cwd() / args.project_name
            self._validated_args = self._validate_args(args)
            self._validate_project_directory(self._project_dir, self._validated_args)
            with status("Generating project files..."):
                self._generate_project_files(self._project_dir, self._validated_args)
        except (ValueError, FileExistsError, Exception) as e:
            cprint(f"Something went wrong during project initialization:\n{e}", Text.WARNING)
            self._revert_generated_files(self._project_dir)
            return ExitCode.ERROR
        else:
            self._display_successful_setup_info(self._project_dir)
            return ExitCode.SUCCESS

    def _validate_args(self, args: Namespace) -> Namespace:
        """Validate the provided arguments."""
        match args.preset:
            case PresetOptions.VERCEL:
                """Enforce postgresql and environment variable configuration for Vercel preset due to platform requirements and security best practices."""
                if args.db == DatabaseBackendOptions.SQLITE:
                    raise ValueError(
                        f"The {PresetOptions.VERCEL} preset requires {DatabaseBackendOptions.POSTGRESQL}."
                    )
                args.db = DatabaseBackendOptions.POSTGRESQL
                args.pg_use_vars = True
            case _:
                """Other presets work with either database. Default to sqlite if args.db is unspecified."""
                if not args.db:
                    args.db = DatabaseBackendOptions.SQLITE

        if args.pg_use_vars and not args.db == DatabaseBackendOptions.POSTGRESQL:
            raise ValueError(
                f"The {DatabaseFlags.USE_VARS} flag is only supported for {DatabaseBackendOptions.POSTGRESQL}."
            )

        return args

    def _validate_project_directory(self, project_dir: Path, args: Namespace) -> None:
        """Check if the project directory already exists and is not empty."""
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
        """Generate project files."""
        from .generate import api_app_py_spec, readme_spec, vercel_json_spec

        main_app_dir = project_dir / args.app
        api_dir = project_dir / "api"

        FileGenerator(readme_spec(path=project_dir / "README.md")).create()
        FileGenerator(api_app_py_spec(path=api_dir / "app.py")).create()

        match args.preset:
            case PresetOptions.VERCEL:
                FileGenerator(vercel_json_spec(path=project_dir / "vercel.json")).create()
            case _:
                pass

        files_with_content: list[tuple[Path, str]] = [
            (project_dir / ".gitignore", self._content_gitignore(args)),
            (project_dir / "pyproject.toml", self._content_pyproject_toml(project_dir, args)),
            (main_app_dir / "templates" / args.app / "index.html", self._content_home_index_html()),
            (main_app_dir / "views.py", self._content_home_views_py(args.app)),
            (main_app_dir / "urls.py", self._content_home_urls_py(project_dir, args.app)),
            (main_app_dir / "migrations" / "__init__.py", ""),
            (main_app_dir / "__init__.py", ""),
            (api_dir / "__init__.py", ""),
        ]

        for path, content in files_with_content:
            FileGenerator(FileSpec(path=path, content=content)).create()

    def _revert_generated_files(self, project_dir: Path) -> None:
        """Remove any files that were generated before an error occurred."""
        if project_dir.exists() and project_dir.is_dir() and any(project_dir.iterdir()):
            for item in sorted(project_dir.rglob("*"), reverse=True):
                item.unlink() if item.is_file() else item.rmdir()

    def _display_successful_setup_info(self, project_dir: Path) -> None:
        """Display setup success message."""
        cprint(f"✓ {Package.DISPLAY_NAME} project '{project_dir.name}' initialized successfully!", Text.SUCCESS)

    def _content_gitignore(self, args: Namespace) -> str:
        """Generate the content for .gitignore based on the provided arguments."""
        sqlite = (
            f"\n# SQLite database\n/db.{DatabaseBackendOptions.SQLITE}3\n"
            if args.db == DatabaseBackendOptions.SQLITE
            else ""
        )
        return (
            "# Python-generated files\n"
            "__pycache__/\n"
            "\n"
            "# Virtual environment\n"
            "/.venv/\n"
            f"{sqlite}"
            "\n"
            "# Environment variables file\n"
            "/.env\n"
            "\n"
            "# Static and media files\n"
            "/public/\n"
        )

    def _content_pyproject_toml(self, project_dir: Path, args: Namespace) -> str:
        """Generate the content for pyproject.toml based on the provided arguments."""
        # dependencies
        extras: list[str] = []

        if args.preset == PresetOptions.VERCEL:
            extras.append("vercel")

        if args.db == DatabaseBackendOptions.POSTGRESQL:
            extras.append("psycopg")

        extras_str = f"[{','.join(extras)}]" if extras else ""
        dependencies = f'"{Package.NAME}{extras_str}~={Package.VERSION}"'

        # tool section
        tool_section = f"[tool.{Package.NAME}]\n"
        tool_section += f'{MainAppTomlKeys.MAIN} = "{args.app}"\n'

        if args.wip:
            tool_section += f"{SecurityTomlKeys.WORK_IN_PROGRESS} = true\n"

        if args.db == DatabaseBackendOptions.POSTGRESQL:
            tool_section += (
                f"{DatabaseTomlKeys.MAIN} = {{ "
                f'{DatabaseTomlKeys.BACKEND} = "{DatabaseBackendOptions.POSTGRESQL}", '
                f"{DatabaseTomlKeys.USE_VARS} = "
                f"{'true' if args.pg_use_vars else 'false'} "
                "}\n"
            )

        allowed_hosts = ['"localhost"', '"127.0.0.1"']

        if args.preset == PresetOptions.VERCEL:
            allowed_hosts.append('".vercel.app"')
            tool_section += (
                f"{StorageTomlKeys.MAIN} = {{ "
                f'{StorageTomlKeys.BACKEND} = "{StorageBackendOptions.VERCEL}", '
                f"{StorageTomlKeys.BLOB_TOKEN} = "
                '"get-from-vercel-blob-storage-and-keep-private-via-env-var" '
                "}\n"
            )

        tool_section += f"{SecurityTomlKeys.ALLOWED_HOSTS} = [{', '.join(allowed_hosts)}]\n"
        tool_section += (
            f'{InternationalizationTomlKeys.MAIN} = {{ {InternationalizationTomlKeys.TIME_ZONE} = "UTC" }}\n'
        )

        # final content
        return (
            "[project]\n"
            f'name = "{project_dir.name}"\n'
            'version = "0.1.0"\n'
            'description = ""\n'
            'readme = "README.md"\n'
            'requires-python = ">=3.14"\n'
            f"dependencies = [{dependencies}]\n"
            "\n"
            "[dependency-groups]\n"
            'dev = ["djlint>=1.36.4"]\n'
            "\n"
            "[tool.djlint]\n"
            'blank_line_before_tag = "block,if,for"\n'
            'blank_line_after_tag = "endblock,endif,endfor"\n'
            "\n"
            f"{tool_section}"
        )

    def _content_home_views_py(self, app_name: str) -> str:
        """Generate the content for the views.py."""
        return (
            "from django.views.generic.base import TemplateView\n\n\n"
            "class HomeView(TemplateView):\n"
            f'    template_name = "{app_name}/index.html"\n'
        )

    def _content_home_urls_py(self, project_dir: Path, app_name: str) -> str:
        """Generate the content for the urls.py."""
        return (
            f'"""\n'
            f"URL configuration for {project_dir.name} project.\n\n"
            f"The `urlpatterns` list routes URLs to views. For more information please see:\n"
            f"    https://docs.djangoproject.com/en/stable/topics/http/urls/\n"
            f'"""\n'
            "from django.urls import path\n\n"
            "from . import views\n\n"
            "urlpatterns = [\n"
            f'    path("", views.HomeView.as_view(), name="{app_name}"),\n'
            "]\n"
        )

    def _content_home_index_html(self) -> str:
        """Generate the content for the index.html."""
        return (
            '{% extends "base/index.html" %}\n\n'
            "{% block fonts %}\n"
            '    <link href="https://fonts.googleapis.com" rel="preconnect" />\n'
            '    <link href="https://fonts.gstatic.com" rel="preconnect" crossorigin />\n'
            '    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Raleway:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Mulish:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"\n'
            '          rel="stylesheet" />\n'
            "{% endblock fonts %}\n\n"
            "{% block main %}\n"
            "    <main>\n"
            '        <section class="container-full py-8">\n'
            '            <p class="text-accent">Welcome to our App!</p>\n'
            "        </section>\n"
            "    </main>\n"
            "{% endblock main %}\n"
        )
