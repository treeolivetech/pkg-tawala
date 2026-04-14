from argparse import ArgumentParser, Namespace
from pathlib import Path

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

from tawala import (
    BASE_CONF,
    DatabaseKeys,
    DatabaseOptions,
    InternationalizationKeys,
    LayoutKeys,
    LayoutOptions,
    PresetBlobTokenDefaults,
    PresetKeys,
    PresetOptions,
    SecurityKeys,
)

__all__ = ["StartProject"]


class StartProject(BaseCommand):
    """Command to initialize a new project."""

    _project_dir: Path
    _validated_args: Namespace
    _project_dir_existed_before: bool
    prog = f"create-tawala-app"
    help = f"Initialize a new {BASE_CONF.pkg_display_name} app."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser."""
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
            f"--{DatabaseKeys.USE_VARS}",
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
                setattr(args, DatabaseKeys.USE_VARS, True)
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
            getattr(args, DatabaseKeys.USE_VARS)
            and not getattr(args, DatabaseKeys.DB) == DatabaseOptions.POSTGRESQL
        ):
            raise ValueError(
                f"The --{DatabaseKeys.USE_VARS} flag is only supported for {DatabaseOptions.POSTGRESQL}."
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

        match getattr(args, PresetKeys.PRESET):
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
                app_dir / "templates" / "app" / "layout.html",
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
            f"✓ {BASE_CONF.pkg_display_name} project '{project_dir.name}' initialized successfully!",
            Text.SUCCESS,
        )

    def _content_gitignore(self, args: Namespace) -> str:
        """Generate .gitignore content."""
        sqlite = (
            f"\n# SQLite database\n/db.{DatabaseOptions.DEFAULT_SQLITE}3\n"
            if getattr(args, DatabaseKeys.DB) == DatabaseOptions.DEFAULT_SQLITE
            else ""
        )
        vercel = (
            "\n# Vercel deployment files\n/.vercel/\n"
            if getattr(args, PresetKeys.PRESET) == PresetOptions.VERCEL
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
        preset = getattr(args, PresetKeys.PRESET)
        db_backend = getattr(args, DatabaseKeys.DB)
        pg_use_vars = getattr(args, DatabaseKeys.USE_VARS)
        is_vercel = preset == PresetOptions.VERCEL
        uses_postgresql = db_backend == DatabaseOptions.POSTGRESQL
        layout = getattr(args, LayoutKeys.LAYOUT)

        extras: list[str] = []
        if is_vercel:
            extras.append("vercel")
        if uses_postgresql:
            extras.append("psycopg")

        extras_suffix = f"[{','.join(extras)}]" if extras else ""
        dependencies = f'"{BASE_CONF.pkg_name}{extras_suffix}"'

        allowed_hosts = ['"localhost"', '"127.0.0.1"']
        tool_lines = [
            f"[tool.{BASE_CONF.pkg_name}]",
            (
                f"{InternationalizationKeys.INTERNATIONALIZATION} = "
                f'{{ {InternationalizationKeys.TIME_ZONE} = "UTC" }}'
            ),
        ]

        if is_vercel:
            allowed_hosts.append('".vercel.app"')
            tool_lines.append(
                f"{PresetKeys.PRESET} = {{ "
                f'{PresetKeys.BACKEND} = "{PresetOptions.VERCEL}", '
                f'{PresetKeys.BLOB_TOKEN} = "{PresetBlobTokenDefaults.GET_FROM_VERCEL}" '
                "}"
            )
        elif uses_postgresql:
            tool_lines.append(
                f"{DatabaseKeys.DB} = {{ "
                f'{DatabaseKeys.BACKEND} = "{DatabaseOptions.POSTGRESQL}", '
                f"{DatabaseKeys.USE_VARS} = "
                f"{'true' if pg_use_vars else 'false'} "
                "}"
            )

        if layout == LayoutOptions.WIP:
            tool_lines.append(
                f"{LayoutKeys.LAYOUT} = {{ "
                f'{LayoutKeys.BACKEND} = "{LayoutOptions.WIP}" '
                "}"
            )

        tool_lines.append(
            f"{SecurityKeys.ALLOWED_HOSTS} = [{', '.join(allowed_hosts)}]"
        )
        tool_section = "\n".join(tool_lines) + "\n"

        uv_source = (
            f"{BASE_CONF.pkg_name} = {{ "
            f'git = "https://github.com/treeolivetech/pkg-{BASE_CONF.pkg_name}.git", '
            f'tag = "{BASE_CONF.pkg_version}" '
            "}\n"
        )

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
            "[tool.uv.sources]\n"
            f"{uv_source}"
            "\n"
            f"{tool_section}"
        )

    def _content_home_views_py(self, app_name: str) -> str:
        """Generate app view module content."""
        return (
            "from django.views.generic.base import TemplateView\n\n\n"
            "class HomeView(TemplateView):\n"
            f'    template_name = "{app_name}/layout.html"\n'
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
            '{% extends "base/layout.html" %}\n'
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
            f"from {BASE_CONF.pkg_name}.management.api.asgi import application\n\n"
            "app = application\n"
        )

    def _content_api_wsgi_py(self) -> str:
        """Generate WSGI entry-point file content."""
        return (
            f"from {BASE_CONF.pkg_name}.management.api.wsgi import application\n\n"
            "app = application\n"
        )

    def _content_vercel_json(self) -> str:
        """Generate vercel.json content for Vercel preset."""
        lines = [
            "{",
            '  "$schema": "https://openapi.vercel.sh/vercel.json",',
            '  "framework": null,',
            f'  "installCommand": "uv run {BASE_CONF.pkg_name} runinstall",',
            f'  "buildCommand": "uv run {BASE_CONF.pkg_name} runbuild",',
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
