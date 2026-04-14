"""Management command for initializing new projects."""

from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import argv

from christianwhocodes import (
    BaseCommand,
    ExitCode,
    FileGenerator,
    FileSpec,
    PostgresFilename,
    Text,
    cprint,
    status,
)

from ... import CONF
from .. import (
    DatabaseFlags,
    DatabaseKeys,
    DatabaseOptions,
    InternationalizationKeys,
    PresetFlags,
    PresetKeys,
    PresetOptions,
    SecurityKeys,
)


class Command(BaseCommand):
    """Command to initialize a new project."""

    _project_dir: Path
    _validated_args: Namespace
    _project_dir_existed_before: bool
    prog = f"{CONF.pkg_name} startproject"
    help = f"Initialize a new {CONF.pkg_display_name} project."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser."""
        parser.add_argument(
            "project_name",
            help=(
                "Name of the project to initialize. Can also be '.' to initialize in the current directory."
            ),
        )

        parser.add_argument(
            PresetFlags.PRESET,
            choices=[p for p in PresetOptions],
            default=PresetOptions.DEFAULT,
            help=f"Preset to use. Defaults to the '{PresetOptions.DEFAULT}' preset.",
        )

        parser.add_argument(
            DatabaseFlags.DB,
            choices=[db for db in DatabaseOptions],
            help=(
                "Database backend to use. Defaults to SQLite if not specified. "
                f"Note: the {PresetOptions.VERCEL} preset automatically uses {DatabaseOptions.POSTGRESQL}. "
                "Other presets work with either database backend, "
                "so choose based on your needs and preferences. "
                f"Defaults to {DatabaseOptions.SQLITE} if not specified."
            ),
        )

        parser.add_argument(
            DatabaseFlags.PG_USE_VARS,
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
            "--wip",
            "--work-in-progress",
            dest="wip",
            action="store_true",
            help="Initialize the project in Work-In-Progress mode.",
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
        match getattr(args, PresetFlags.PRESET.dest):
            case PresetOptions.VERCEL:
                # Enforce postgresql and environment variable configuration for Vercel preset
                # due to platform requirements and security best practices.
                if getattr(args, DatabaseFlags.DB.dest) == DatabaseOptions.SQLITE:
                    raise ValueError(
                        f"The {PresetOptions.VERCEL} preset requires {DatabaseOptions.POSTGRESQL}."
                    )
                setattr(args, DatabaseFlags.DB.dest, DatabaseOptions.POSTGRESQL)
                setattr(args, DatabaseFlags.PG_USE_VARS.dest, True)
            case _:
                # Other presets work with either database.
                # Default to sqlite if getattr(args, DatabaseFlags.DB.dest) is unspecified.
                if not getattr(args, DatabaseFlags.DB.dest):
                    setattr(args, DatabaseFlags.DB.dest, DatabaseOptions.SQLITE)

        if (
            getattr(args, DatabaseFlags.PG_USE_VARS.dest)
            and not getattr(args, DatabaseFlags.DB.dest) == DatabaseOptions.POSTGRESQL
        ):
            raise ValueError(
                f"The {DatabaseFlags.PG_USE_VARS} flag is only supported for {DatabaseOptions.POSTGRESQL}."
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
        """Create all project files and folders for the selected options."""
        app_dir = project_dir / "app"
        api_dir = project_dir / "api"

        match getattr(args, PresetFlags.PRESET.dest):
            case PresetOptions.VERCEL:
                vercel_json_spec = FileSpec(
                    path=project_dir / "vercel.json",
                    content=self._content_vercel_json(),
                )
                FileGenerator(vercel_json_spec).create()
            case _:
                pass

        content_files: list[tuple[Path, str]] = [
            (api_dir / "__init__.py", '"""API module."""'),
            (api_dir / "asgi.py", self._content_api_asgi_py()),
            (api_dir / "wsgi.py", self._content_api_wsgi_py()),
            (project_dir / ".gitignore", self._content_gitignore(args)),
            (
                project_dir / "pyproject.toml",
                self._content_pyproject_toml(project_dir, args),
            ),
            (app_dir / "__init__.py", '"""Main App module."""'),
            (
                app_dir / "templates" / "app" / "index.html",
                self._content_home_index_html(),
            ),
            (app_dir / "views.py", self._content_home_views_py("app")),
            (app_dir / "urls.py", self._content_home_urls_py(project_dir, "app")),
            (app_dir / "migrations" / "__init__.py", '"""App migrations."""'),
            (project_dir / "README.md", self._content_readme_md(project_dir)),
        ]

        for path, content in content_files:
            FileGenerator(FileSpec(path=path, content=content)).create()

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
            f"✓ {CONF.pkg_display_name} project '{project_dir.name}' initialized successfully!",
            Text.SUCCESS,
        )

    def _content_gitignore(self, args: Namespace) -> str:
        """Generate .gitignore content."""
        sqlite = (
            f"\n# SQLite database\n/db.{DatabaseOptions.SQLITE}3\n"
            if getattr(args, DatabaseFlags.DB.dest) == DatabaseOptions.SQLITE
            else ""
        )
        vercel = (
            "\n# Vercel deployment files\n/.vercel/\n"
            if getattr(args, PresetFlags.PRESET.dest) == PresetOptions.VERCEL
            else ""
        )

        return (
            "# Python-generated files\n"
            "__pycache__/\n"
            "\n"
            "# Virtual environment\n"
            "/.venv/\n"
            f"{sqlite}"
            f"{vercel}"
            "\n"
            "# Environment variables file\n"
            "/.env\n"
            "\n"
            "# Static and media files\n"
            "/public/\n"
        )

    def _content_pyproject_toml(self, project_dir: Path, args: Namespace) -> str:
        """Generate pyproject.toml content for the initialized project."""
        # dependencies
        _extras: list[str] = []

        if getattr(args, PresetFlags.PRESET.dest) == PresetOptions.VERCEL:
            _extras.append("vercel")

        if getattr(args, DatabaseFlags.DB.dest) == DatabaseOptions.POSTGRESQL:
            _extras.append("psycopg")

        dependencies = f'"{CONF.pkg_name}{f"[{','.join(_extras)}]" if _extras else ""}"'

        # tool section
        tool_section = f"[tool.{CONF.pkg_name}]\n"
        _allowed_hosts = ['"localhost"', '"127.0.0.1"']

        tool_section += (
            f"{InternationalizationKeys.INTERNATIONALIZATION} = "
            f'{{ {InternationalizationKeys.TIME_ZONE} = "UTC" }}\n'
        )

        if getattr(args, PresetFlags.PRESET.dest) == PresetOptions.VERCEL:
            _allowed_hosts.append('".vercel.app"')
            tool_section += (
                f"{PresetKeys.PRESET} = {{ "
                f'{PresetKeys.BACKEND} = "{PresetOptions.VERCEL}", '
                f"{PresetKeys.BLOB_TOKEN} = "
                '"get-from-vercel-blob-storage-and-keep-private-via-env-var" '
                "}\n"
            )

        if getattr(args, PresetFlags.PRESET.dest) == PresetOptions.VERCEL:
            # Vercel preset always uses PostgreSQL with environment variable configuration.
            # See config/startproject.py for details.
            pass
        elif getattr(args, DatabaseFlags.DB.dest) == DatabaseOptions.POSTGRESQL:
            tool_section += (
                f"{DatabaseKeys.DB} = {{ "
                f'{DatabaseKeys.BACKEND} = "{DatabaseOptions.POSTGRESQL}", '
                f"{DatabaseKeys.USE_VARS} = "
                f"{'true' if getattr(args, DatabaseFlags.PG_USE_VARS.dest) else 'false'} "
                "}\n"
            )

        if args.wip:
            tool_section += f"{SecurityKeys.WORK_IN_PROGRESS} = true\n"

        tool_section += (
            f"{SecurityKeys.ALLOWED_HOSTS} = [{', '.join(_allowed_hosts)}]\n"
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
            f"{tool_section}"
        )

    def _content_home_views_py(self, app_name: str) -> str:
        """Generate app view module content."""
        return (
            "from django.views.generic.base import TemplateView\n\n\n"
            "class HomeView(TemplateView):\n"
            f'    template_name = "{app_name}/index.html"\n'
        )

    def _content_home_urls_py(self, project_dir: Path, app_name: str) -> str:
        """Generate app URL configuration content."""
        return (
            f'"""URL configuration for {project_dir.name} project.\n\n'
            "The `urlpatterns` list routes URLs to views. For more information please see:\n"
            "    https://docs.djangoproject.com/en/stable/topics/http/urls/\n"
            '"""\n\n'
            "from django.urls import path\n\n"
            "from . import views\n\n"
            "urlpatterns = [\n"
            f'    path("", views.HomeView.as_view(), name="home"),\n'
            "]\n"
        )

    def _content_home_index_html(self) -> str:
        """Generate starter home page template content."""
        return (
            '{% extends "core/index.html" %}\n'
            "{% block fonts %}\n"
            '    <link href="https://fonts.googleapis.com" rel="preconnect" />\n'
            '    <link href="https://fonts.gstatic.com" rel="preconnect" crossorigin />\n'
            '    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Raleway:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Mulish:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"\n'
            '          rel="stylesheet" />\n'
            "{% endblock fonts %}\n"
            "{% block main %}\n"
            "    <main>\n"
            '        <section class="container">\n'
            '            <p class="text-primary">Welcome to our App!</p>\n'
            "        </section>\n"
            "    </main>\n"
            "{% endblock main %}\n"
        )

    def _content_api_asgi_py(self) -> str:
        """Generate ASGI entry-point file content."""
        return (
            f"from {CONF.pkg_name}.management.api.asgi import application\n\n"
            "app = application\n"
        )

    def _content_api_wsgi_py(self) -> str:
        """Generate WSGI entry-point file content."""
        return (
            f"from {CONF.pkg_name}.management.api.wsgi import application\n\n"
            "app = application\n"
        )

    def _content_vercel_json(self) -> str:
        """Generate vercel.json content for Vercel preset."""
        lines = [
            "{",
            '  "$schema": "https://openapi.vercel.sh/vercel.json",',
            '  "framework": null,',
            f'  "installCommand": "uv run {CONF.pkg_name} runinstall",',
            f'  "buildCommand": "uv run {CONF.pkg_name} runbuild",',
            '  "rewrites": [',
            "    {",
            '      "source": "/(.*)",',
            '      "destination": "/api/asgi.py"',
            "    }",
            "  ]",
            "}",
        ]
        return "\n".join(lines) + "\n"

    def _content_readme_md(self, project_dir: Path) -> str:
        """Generate README content for the initialized project."""
        return f"# {project_dir.name}\n"


def main(args: list[str] | None = None) -> ExitCode | int:
    """Execute the project initialization command."""
    command_args = argv[1:] if args is None else args
    if command_args and command_args[0] in ["-v", "--ver", "--version", "version"]:
        from christianwhocodes import print_version

        return print_version(CONF.pkg_name)
    return Command()(command_args)


if __name__ == "__main__":
    raise SystemExit(main())
