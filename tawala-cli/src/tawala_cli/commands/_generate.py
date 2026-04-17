"""`generate` command/script."""

from argparse import ArgumentParser, Namespace
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, cast

from christianwhocodes import (
    BaseCommand,
    ExitCode,
    FileGenerator,
    FileSpec,
    Version,
    cprint,
)

from tawala import (
    DATABASES_SCHEMA,
    INTERNATIONALIZATION_SCHEMA,
    LAYOUT_SCHEMA,
    PRESETS_SCHEMA,
    PROJECT_CONF,
    RUNCOMMANDS_SCHEMA,
    SECURITY_SCHEMA,
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

__all__ = ["GenerateCommand"]


class _GenerateTargets:
    """File-generation targets available under the generate command."""

    ALL = "all"
    API_INIT = "api-init"
    API_ASGI = "api-asgi"
    API_WSGI = "api-wsgi"
    GITIGNORE = "gitignore"
    PYPROJECT = "pyproject"
    APP_INIT = "app-init"
    APP_LAYOUT = "app-layout"
    APP_VIEWS = "app-views"
    APP_URLS = "app-urls"
    APP_MIGRATIONS_INIT = "app-migrations-init"
    README = "readme"
    VERCEL_JSON = "vercel-json"
    CONFIG_MD = "config-md"

    CHOICES = [
        ALL,
        API_INIT,
        API_ASGI,
        API_WSGI,
        GITIGNORE,
        PYPROJECT,
        APP_INIT,
        APP_LAYOUT,
        APP_VIEWS,
        APP_URLS,
        APP_MIGRATIONS_INIT,
        README,
        VERCEL_JSON,
        CONFIG_MD,
    ]


class GenerateCommand(BaseCommand):
    """Generate one or more scaffold files for a Tawala project."""

    prog = PROJECT_CONF.cli_pkg_name
    help = "Generate scaffold artifacts (files/docs) for a Tawala project."

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
            "target",
            choices=_GenerateTargets.CHOICES,
            help="Which artifact to generate. Use 'all' to generate a full scaffold set.",
        )

        parser.add_argument(
            "--output-dir",
            default=".",
            help="Output directory where files should be generated. Defaults to current directory.",
        )

        parser.add_argument(
            "--project-name",
            help="Project name used by generated files. Defaults to output directory name.",
        )

        parser.add_argument(
            f"--{PresetKeys.PRESET}",
            choices=list(PresetOptions),
            default=PresetOptions.DEFAULT,
            help=f"Preset to use. Defaults to '{PresetOptions.DEFAULT}'.",
        )

        parser.add_argument(
            f"--{DatabaseKeys.DB}",
            choices=list(DatabaseOptions),
            help=(
                "Database backend to use. Defaults to SQLite if not specified. "
                f"The {PresetOptions.VERCEL} preset always resolves to {DatabaseOptions.POSTGRESQL}."
            ),
        )

        parser.add_argument(
            f"--{DatabaseKeys.USE_VARS_OPTION}",
            action="store_true",
            help=(
                "Use env/pyproject variables for PostgreSQL configuration. "
                f"Only valid with {DatabaseOptions.POSTGRESQL}."
            ),
        )

        parser.add_argument(
            f"--{LayoutKeys.LAYOUT}",
            choices=list(LayoutOptions),
            help="Layout to use for generated files.",
        )

    def handle(self, args: Namespace) -> ExitCode:
        """Execute generation logic."""
        try:
            output_dir = Path(args.output_dir).resolve()
            output_dir.mkdir(parents=True, exist_ok=True)

            validated_args = self._validate_args(args)
            project_name = args.project_name or output_dir.name
            app_name = "app"

            specs = self._build_specs(
                target=args.target,
                output_dir=output_dir,
                project_name=project_name,
                app_name=app_name,
                args=validated_args,
            )

            for spec in specs:
                FileGenerator(spec).create()
        except Exception as e:
            cprint(f"Generation failed: {e}")
            return ExitCode.ERROR

        return ExitCode.SUCCESS

    def _validate_args(self, args: Namespace) -> Namespace:
        """Apply argument cross-field validation and defaults."""
        match getattr(args, PresetKeys.PRESET):
            case PresetOptions.VERCEL:
                if getattr(args, DatabaseKeys.DB) == DatabaseOptions.DEFAULT_SQLITE:
                    raise ValueError(
                        f"The {PresetOptions.VERCEL} preset requires {DatabaseOptions.POSTGRESQL}."
                    )
                setattr(args, DatabaseKeys.DB, DatabaseOptions.POSTGRESQL)
                setattr(args, DatabaseKeys.USE_VARS_OPTION, True)
            case _:
                if not getattr(args, DatabaseKeys.DB):
                    setattr(args, DatabaseKeys.DB, DatabaseOptions.DEFAULT_SQLITE)

        if (
            getattr(args, DatabaseKeys.USE_VARS_OPTION)
            and getattr(args, DatabaseKeys.DB) != DatabaseOptions.POSTGRESQL
        ):
            raise ValueError(
                f"The --{DatabaseKeys.USE_VARS_OPTION} flag is only supported for {DatabaseOptions.POSTGRESQL}."
            )

        return args

    def _build_specs(
        self,
        target: str,
        output_dir: Path,
        project_name: str,
        app_name: str,
        args: Namespace,
    ) -> list[FileSpec]:
        """Create file specs for the requested target."""
        app_dir = output_dir / app_name
        api_dir = output_dir / "api"

        base_specs: dict[str, FileSpec] = {
            _GenerateTargets.API_INIT: FileSpec(
                path=api_dir / "__init__.py", content='"""API module."""'
            ),
            _GenerateTargets.API_ASGI: FileSpec(
                path=api_dir / "asgi.py", content=self._content_api_asgi_py()
            ),
            _GenerateTargets.API_WSGI: FileSpec(
                path=api_dir / "wsgi.py", content=self._content_api_wsgi_py()
            ),
            _GenerateTargets.GITIGNORE: FileSpec(
                path=output_dir / ".gitignore", content=self._content_gitignore(args)
            ),
            _GenerateTargets.PYPROJECT: FileSpec(
                path=output_dir / "pyproject.toml",
                content=self._content_pyproject_toml(project_name, args),
            ),
            _GenerateTargets.APP_INIT: FileSpec(
                path=app_dir / "__init__.py", content='"""Main App module."""'
            ),
            _GenerateTargets.APP_LAYOUT: FileSpec(
                path=app_dir / "templates" / app_name / "layout.html",
                content=self._content_home_index_html(),
            ),
            _GenerateTargets.APP_VIEWS: FileSpec(
                path=app_dir / "views.py", content=self._content_home_views_py(app_name)
            ),
            _GenerateTargets.APP_URLS: FileSpec(
                path=app_dir / "urls.py",
                content=self._content_home_urls_py(project_name, app_name),
            ),
            _GenerateTargets.APP_MIGRATIONS_INIT: FileSpec(
                path=app_dir / "migrations" / "__init__.py",
                content='"""App migrations."""',
            ),
            _GenerateTargets.README: FileSpec(
                path=output_dir / "README.md",
                content=self._content_readme_md(project_name),
            ),
            _GenerateTargets.VERCEL_JSON: FileSpec(
                path=output_dir / "vercel.json",
                content=self._content_vercel_json(),
            ),
            _GenerateTargets.CONFIG_MD: FileSpec(
                path=output_dir / "CONFIG.md", content=self._content_config_md()
            ),
        }

        if target != _GenerateTargets.ALL:
            return [base_specs[target]]

        ordered_targets = [
            _GenerateTargets.API_INIT,
            _GenerateTargets.API_ASGI,
            _GenerateTargets.API_WSGI,
            _GenerateTargets.GITIGNORE,
            _GenerateTargets.PYPROJECT,
            _GenerateTargets.APP_INIT,
            _GenerateTargets.APP_LAYOUT,
            _GenerateTargets.APP_VIEWS,
            _GenerateTargets.APP_URLS,
            _GenerateTargets.APP_MIGRATIONS_INIT,
            _GenerateTargets.README,
            _GenerateTargets.CONFIG_MD,
        ]
        if getattr(args, PresetKeys.PRESET) == PresetOptions.VERCEL:
            ordered_targets.append(_GenerateTargets.VERCEL_JSON)

        return [base_specs[target_name] for target_name in ordered_targets]

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

    def _content_pyproject_toml(self, project_name: str, args: Namespace) -> str:
        """Generate pyproject.toml content for the initialized project."""
        preset = getattr(args, PresetKeys.PRESET)
        db_backend = getattr(args, DatabaseKeys.DB)
        pg_use_vars = getattr(args, DatabaseKeys.USE_VARS_OPTION)
        is_vercel = preset == PresetOptions.VERCEL
        uses_postgresql = db_backend == DatabaseOptions.POSTGRESQL
        layout = getattr(args, LayoutKeys.LAYOUT)

        extras: list[str] = []
        if is_vercel:
            extras.append("vercel")
        if uses_postgresql:
            extras.append("psycopg")

        extras_suffix = f"[{','.join(extras)}]" if extras else ""
        dependencies = f'"{PROJECT_CONF.pkg_name}{extras_suffix}"'

        allowed_hosts = ['"localhost"', '"127.0.0.1"']
        tool_lines = [
            f"[tool.{PROJECT_CONF.pkg_name}]",
            (
                f"{InternationalizationKeys.INTERNATIONALIZATION} = "
                f'{{ {InternationalizationKeys.TIME_ZONE} = "UTC" }}'
            ),
        ]

        if is_vercel:
            allowed_hosts.append('".vercel.app"')
            tool_lines.append(
                f"{PresetKeys.PRESET} = {{ "
                f'{PresetKeys.OPTION} = "{PresetOptions.VERCEL}", '
                f'{PresetKeys.BLOB_TOKEN} = "{PresetBlobTokenDefaults.GET_FROM_VERCEL}" '
                "}"
            )
        elif uses_postgresql:
            tool_lines.append(
                f"{DatabaseKeys.DB} = {{ "
                f'{DatabaseKeys.OPTION} = "{DatabaseOptions.POSTGRESQL}", '
                f"{DatabaseKeys.USE_VARS_OPTION} = "
                f"{'true' if pg_use_vars else 'false'} "
                "}"
            )

        if layout == LayoutOptions.WIP:
            tool_lines.append(
                f"{LayoutKeys.LAYOUT} = {{ "
                f'{LayoutKeys.OPTION} = "{LayoutOptions.WIP}" '
                "}"
            )

        tool_lines.append(
            f"{SecurityKeys.ALLOWED_HOSTS} = [{', '.join(allowed_hosts)}]"
        )
        tool_section = "\n".join(tool_lines) + "\n"

        uv_source = (
            f"{PROJECT_CONF.pkg_name} = {{ "
            f'git = "https://github.com/treeolivetech/pkg-{PROJECT_CONF.pkg_name}.git", '
            f'tag = "{PROJECT_CONF.pkg_version}" '
            "}\n"
        )

        return (
            "[project]\n"
            f'name = "{project_name}"\n'
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

    def _content_home_urls_py(self, project_name: str, app_name: str) -> str:
        """Generate app URL configuration content."""
        return (
            f'"""URL configuration for {project_name} project.\n\n'
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
            f"from {PROJECT_CONF.pkg_name}.management.api.asgi import application\n\n"
            "app = application\n"
        )

    def _content_api_wsgi_py(self) -> str:
        """Generate WSGI entry-point file content."""
        return (
            f"from {PROJECT_CONF.pkg_name}.management.api.wsgi import application\n\n"
            "app = application\n"
        )

    def _content_vercel_json(self) -> str:
        """Generate vercel.json content for Vercel preset."""
        lines = [
            "{",
            '  "$schema": "https://openapi.vercel.sh/vercel.json",',
            '  "framework": null,',
            f'  "installCommand": "uv run {PROJECT_CONF.pkg_name} runinstall",',
            f'  "buildCommand": "uv run {PROJECT_CONF.pkg_name} runbuild",',
            '  "rewrites": [',
            "    {",
            '      "source": "/(.*)",',
            '      "destination": "/api/asgi.py"',
            "    }",
            "  ]",
            "}",
        ]
        return "\n".join(lines) + "\n"

    def _content_readme_md(self, project_name: str) -> str:
        """Generate README content for the initialized project."""
        return f"# {project_name}\n"

    def _content_config_md(self) -> str:
        """Generate CONFIG.md documentation from exported setting schemas."""
        generated_on = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")
        lines = [
            "# Tawala Configuration Reference",
            "",
            "A generated reference of all supported `tool.tawala` settings, their defaults, and allowed values.",
            "",
            f"Generated on: {generated_on}",
            "",
            "## Source Priority",
            "",
            "Configuration is resolved in this order:",
            "1. Environment variables",
            "2. `pyproject.toml` in `[tool.tawala]`",
            "3. Schema defaults",
            "",
        ]

        sections: list[tuple[str, dict[str, Any]]] = [
            ("Security & Deployment", SECURITY_SCHEMA),
            ("Presets & Storages", PRESETS_SCHEMA),
            ("Databases", DATABASES_SCHEMA),
            ("Layout", LAYOUT_SCHEMA),
            ("Internationalization", INTERNATIONALIZATION_SCHEMA),
            ("Runcommands", RUNCOMMANDS_SCHEMA),
        ]

        for title, schema in sections:
            lines.extend([
                f"## {title}",
                "",
                "| Key | TOML Path | ENV | Type | Default | Options | Description |",
                "|---|---|---|---|---|---|---|",
            ])

            for key, field in schema.items():
                key_str = self._format_for_markdown(str(key))
                toml_str = self._format_for_markdown(str(field.toml))
                env_str = self._format_for_markdown(str(field.env))
                type_str = self._format_for_markdown(field.type.__name__)
                default_str = self._format_for_markdown(
                    self._display_value(field.default)
                )
                options_str = self._format_for_markdown(
                    ", ".join(self._display_value(option) for option in field.options)
                    if field.options
                    else "-"
                )
                help_str = self._format_for_markdown(field.help_text or "-")
                lines.append(
                    f"| {key_str} | {toml_str} | {env_str} | {type_str} | {default_str} | {options_str} | {help_str} |"
                )

            lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    def _display_value(self, value: Any) -> str:
        """Convert values into compact human-readable markdown text."""
        if isinstance(value, Enum):
            return self._display_value(value.value)
        if isinstance(value, list):
            items = cast(list[Any], value)
            if not value:
                return "[]"
            return "[" + ", ".join(self._display_value(item) for item in items) + "]"
        if isinstance(value, bool):
            return "true" if value else "false"
        if value is None:
            return "null"
        return str(value)

    def _format_for_markdown(self, value: str) -> str:
        """Escape markdown table separators and wrap inline literals."""
        escaped = value.replace("|", "\\|")
        return f"`{escaped}`" if escaped not in {"-", ""} else escaped
