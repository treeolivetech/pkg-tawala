"""Project initialization command."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from christianwhocodes import BaseCommand, ExitCode, FileGenerator, FileSpec, InitAction, PostgresFilename, Text, cprint, status

from .... import (
    DatabaseChoices,
    DatabaseTomlKeys,
    Package,
    PostgresFlags,
    PresetChoices,
    Project,
    StorageChoices,
    StorageTomlKeys,
    SecurityTomlKeys,
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
            "project_name", help="Name of the project to initialize. Can also be '.' to initialize in the current directory."
        )
        parser.add_argument(
            "-p",
            "--preset",
            dest="preset",
            type=PresetChoices,
            choices=[p for p in PresetChoices],
            help="Project preset to use. Defaults to the 'default' preset.",
            default=PresetChoices.DEFAULT,
        )
        parser.add_argument(
            "-d",
            "--db",
            dest="db",
            type=DatabaseChoices,
            choices=[db for db in DatabaseChoices],
            help=(
                "Database backend to use.  Defaults to SQLite if not specified. "
                f"Note: the {PresetChoices.VERCEL} preset automatically uses {DatabaseChoices.POSTGRESQL}. "
                f"Other presets work with either database backend, so choose based on your needs and preferences. Defaults to {DatabaseChoices.SQLITE} if not specified."
            ),
        )
        parser.add_argument(
            PostgresFlags.USE_VARS,
            action="store_true",
            help=(
                f"Use environment / pyproject.toml variables for PostgreSQL configuration. If False, configuration will be read from {PostgresFilename.PGSERVICE} and {PostgresFilename.PGPASS} files."
                f"Note: this flag is only applicable if the database backend is set to {DatabaseChoices.POSTGRESQL}. "
                f"The {PresetChoices.VERCEL} preset automatically sets this flag to True since Vercel requires environment variable configuration for PostgreSQL and does not support file-based configuration."
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
            self._validated_args = self._validate_args(args)
            self._validate_project_directory(self._project_dir, self._validated_args)
            with status("Generating base project files..."):
                self._generate_base_files(self._project_dir, self._validated_args)
            with status("Generating preset files..."):
                self._generate_preset_files(self._project_dir, self._validated_args)
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
            case PresetChoices.VERCEL:
                """Enforce postgresql and environment variable configuration for Vercel preset due to platform requirements and security best practices."""
                if args.db == DatabaseChoices.SQLITE:
                    raise ValueError(f"The {PresetChoices.VERCEL} preset requires {DatabaseChoices.POSTGRESQL}.")
                args.db = DatabaseChoices.POSTGRESQL
                args.pg_use_vars = True
            case _:
                """Other presets work with either database. Default to sqlite if args.db is unspecified."""
                if not args.db:
                    args.db = DatabaseChoices.SQLITE
        if args.pg_use_vars and not args.db == DatabaseChoices.POSTGRESQL:
            raise ValueError(f"The {PostgresFlags.USE_VARS} flag is only supported for {DatabaseChoices.POSTGRESQL}.")
        return args

    def _validate_project_directory(self, project_dir: Path, args: Namespace) -> None:
        """Check if the project directory already exists and is not empty."""
        if args.project_name == "." and any(project_dir.iterdir()):
            raise FileExistsError(
                "The current directory is not empty. Please choose a different project name or remove the existing files."
            )
        if not project_dir.exists():
            return
        if project_dir.is_file():
            raise FileExistsError(
                f"A file named '{project_dir}' already exists. Please choose a different project name or remove the existing file."
            )
        if any(project_dir.iterdir()):
            raise FileExistsError(
                f"The directory '{project_dir}' already exists and is not empty. Please choose a different project name or remove the existing files in the directory."
            )

    def _generate_base_files(self, project_dir: Path, args: Namespace) -> None:
        """Generate base project files."""
        # TODO: Test out using call_command 'startapp' for generating the home app files instead of manually creating them here. It would be ideal to leverage Django's built-in app generation logic if possible to reduce the amount of custom code we need to maintain for generating app files.
        home_app_dir: Path = project_dir / "home"
        files_with_content: list[tuple[Path, str]] = [
            (project_dir / "pyproject.toml", self._get_pyproject_toml_content(project_dir, args)),
            (project_dir / ".gitignore", self._get_gitignore_content(args)),
            (home_app_dir / "__init__.py", ""),
            (home_app_dir / "migrations" / "__init__.py", ""),
            (home_app_dir / "templates" / Project.HOME_APP_NAME / "index.html", self._get_home_app_index_html_content()),
            (home_app_dir / "apps.py", self._get_home_app_apps_py_content()),
            (home_app_dir / "views.py", self._get_home_app_views_py_content()),
            (home_app_dir / "urls.py", self._get_home_app_urls_py_content(project_dir)),
            (home_app_dir / "admin.py", self._get_home_app_admin_py_content()),
            (home_app_dir / "models.py", self._get_home_app_models_py_content()),
            (home_app_dir / "tests.py", self._get_home_app_tests_py_content()),
        ]
        for path, content in files_with_content:
            FileGenerator(FileSpec(path=path, content=content)).create()

    def _generate_preset_files(self, project_dir: Path, args: Namespace) -> None:
        """Generate preset-specific files."""
        from .generate import get_api_server_spec, get_readme_spec, get_vercel_spec

        match args.preset:
            case PresetChoices.VERCEL:
                api_dir: Path = project_dir / "api"
                FileGenerator(get_vercel_spec(path=project_dir / "vercel.json")).create()
                FileGenerator(get_api_server_spec(path=api_dir / "server.py")).create()
                FileGenerator(FileSpec(path=api_dir / "__init__.py", content="")).create()
            case _:
                pass
        FileGenerator(get_readme_spec(path=project_dir / "README.md")).create()

    def _revert_generated_files(self, project_dir: Path) -> None:
        """Remove any files that were generated before an error occurred."""
        if project_dir.exists() and project_dir.is_dir() and any(project_dir.iterdir()):
            for item in sorted(project_dir.rglob("*"), reverse=True):
                item.unlink() if item.is_file() else item.rmdir()

    def _get_pyproject_toml_content(self, project_dir: Path, args: Namespace) -> str:
        """Generate the content for pyproject.toml based on the provided arguments."""
        # dependencies
        extras: list[str] = []
        if args.preset == PresetChoices.VERCEL:
            extras.append("vercel")
        if args.db == DatabaseChoices.POSTGRESQL:
            extras.append("psycopg")
        extras_str = f"[{','.join(extras)}]" if extras else ""
        dependencies = f'"{Package.NAME}{extras_str}>={Package.VERSION}"'
        # tool section
        tool_section = f"[tool.{Package.NAME}]\n"
        if args.wip:
            tool_section += f"{SecurityTomlKeys.WIP} = true\n"
        if args.db == DatabaseChoices.POSTGRESQL:
            tool_section += f'db = {{ {DatabaseTomlKeys.BACKEND} = "{DatabaseChoices.POSTGRESQL}", {DatabaseTomlKeys.USE_VARS} = {"true" if args.pg_use_vars else "false"} }}\n'
        if args.preset == PresetChoices.VERCEL:
            tool_section += f'storage = {{ {StorageTomlKeys.BACKEND} = "{StorageChoices.VERCELBLOB}", {StorageTomlKeys.BLOB_TOKEN} = "get-from-vercel-blob-storage-and-keep-private-via-env-var" }}\n'
        # final content
        return (
            "[project]\n"
            f'name = "{project_dir.name}"\n'
            'version = "0.1.0"\n'
            'description = ""\n'
            'readme = "README.md"\n'
            'requires-python = ">=3.13"\n'
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

    def _get_gitignore_content(self, args: Namespace) -> str:
        """Generate the content for .gitignore based on the provided arguments."""
        sqlite = f"\n# SQLite database\n/db.{DatabaseChoices.SQLITE}3\n" if args.db == DatabaseChoices.SQLITE else ""
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

    def _get_home_app_apps_py_content(self) -> str:
        """Generate the content for the home app apps.py."""
        return 'from django.apps import AppConfig\n\n\nclass HomeConfig(AppConfig):\n    name = "home"\n'

    def _get_home_app_views_py_content(self) -> str:
        """Generate the content for the home app views.py."""
        return (
            "from django.views.generic.base import TemplateView\n\n\n"
            "class HomeView(TemplateView):\n"
            '    template_name = "home/index.html"\n'
        )

    def _get_home_app_urls_py_content(self, project_dir: Path) -> str:
        """Generate the content for the home app urls.py."""
        return (
            f'"""\n'
            f"URL configuration for {project_dir.name} project.\n"
            f"\n"
            f"The `urlpatterns` list routes URLs to views. For more information please see:\n"
            f"    https://docs.djangoproject.com/en/stable/topics/http/urls/\n"
            f"Examples:\n"
            f"Function views\n"
            f"    1. Add an import:  from my_app import views\n"
            f"    2. Add a URL to urlpatterns:  path('', views.home, name='home')\n"
            f"Class-based views\n"
            f"    1. Add an import:  from other_app.views import Home\n"
            f"    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')\n"
            f"Including another URLconf\n"
            f"    1. Import the include() function: from django.urls import include, path\n"
            f"    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))\n"
            f'"""\n'
            "from django.contrib import admin\n"
            "from django.urls import URLPattern, URLResolver, path\n\n"
            "from . import views\n\n"
            "urlpatterns: list[URLPattern | URLResolver] = [\n"
            '    path("admin/", admin.site.urls),\n'
            '    path("", views.HomeView.as_view(), name="home"),\n'
            "]\n"
        )

    def _get_home_app_admin_py_content(self) -> str:
        """Generate the content for the home app admin.py."""
        return "# from django.contrib import admin\n\n# Register your models here.\n"

    def _get_home_app_models_py_content(self) -> str:
        """Generate the content for the home app models.py."""
        return "# from django.db import models\n\n# Create your models here.\n"

    def _get_home_app_tests_py_content(self) -> str:
        """Generate the content for the home app tests.py."""
        return "# from django.test import TestCase\n\n# Create your tests here.\n"

    def _get_home_app_index_html_content(self) -> str:
        """Generate the content for the home app index.html."""
        return (
            '{% extends "base/index.html" %}\n'
            "{% block fonts %}\n"
            '    <link href="https://fonts.googleapis.com" rel="preconnect" />\n'
            '    <link href="https://fonts.gstatic.com" rel="preconnect" crossorigin />\n'
            '    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Raleway:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Mulish:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"\n'
            '          rel="stylesheet" />\n'
            "{% endblock fonts %}\n"
            "{% block main %}\n"
            "    <main>\n"
            '        <section class="container-full py-8">\n'
            '            <p class="text-accent">Welcome to our App!</p>\n'
            "        </section>\n"
            "    </main>\n"
            "{% endblock main %}\n"
        )

    def _display_successful_setup_info(self, project_dir: Path) -> None:
        """Display setup success message."""
        cprint(f"✓ Project '{project_dir.name}' initialized successfully!", Text.SUCCESS)
