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
    cprint,
)

from ..conf import (
    API_PKG_MODULE,
    API_PKG_NAME,
    API_PKG_VERSION,
    DATABASES_SCHEMA,
    FETCH_PROJECT,
    INTERNATIONALIZATION_SCHEMA,
    LAYOUT_SCHEMA,
    PRESET_SCHEMA,
    RUNCOMMANDS_SCHEMA,
    SECURITY_SCHEMA,
    DatabaseHelpTexts,
    DatabaseKeys,
    DatabaseOptions,
    LayoutHelpTexts,
    LayoutKeys,
    LayoutOptions,
    PresetDefaults,
    PresetHelpTexts,
    PresetKeys,
    PresetOptions,
    SecurityKeys,
)

__all__ = ["GenerateCommand"]


class _GenerateTargets:
    """File-generation targets available under the generate command."""

    ALL = "all"
    API_INIT = "api-init"
    API_SERVER = "api-server"
    GITIGNORE = "gitignore"
    PYPROJECT = "pyproject"
    README = "readme"
    VERCEL_JSON = "vercel-json"
    CONFIG_MD = "config-md"

    CHOICES = [
        ALL,
        API_INIT,
        API_SERVER,
        GITIGNORE,
        PYPROJECT,
        README,
        VERCEL_JSON,
        CONFIG_MD,
    ]


class GenerateCommand(BaseCommand):
    """Generate one or more scaffold project files."""

    prog = API_PKG_NAME
    help = "Generate scaffold artifacts (files)."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser."""
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=API_PKG_VERSION,
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
            f"--{PresetKeys.PRESET.value}",
            choices=list(PresetOptions),
            default=PresetDefaults.OPTION.value,
            help=PresetHelpTexts.OPTION.value,
        )

        parser.add_argument(
            f"--{DatabaseKeys.DB.value}",
            choices=list(DatabaseOptions),
            help=DatabaseHelpTexts.OPTION.value,
        )

        parser.add_argument(
            f"--{DatabaseKeys.USE_VARS_OPTION.value}",
            action="store_true",
            help=DatabaseHelpTexts.USE_VARS_OPTION.value,
        )

        parser.add_argument(
            f"--{LayoutKeys.LAYOUT.value}",
            choices=list(LayoutOptions),
            help=LayoutHelpTexts.OPTION.value,
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
        match getattr(args, PresetKeys.PRESET.value):
            case PresetOptions.VERCEL.value:
                if getattr(args, DatabaseKeys.DB.value) == DatabaseOptions.SQLITE.value:
                    raise ValueError(
                        f"The {PresetOptions.VERCEL.value} preset requires {DatabaseOptions.POSTGRESQL.value}."
                    )
                setattr(args, DatabaseKeys.DB, DatabaseOptions.POSTGRESQL.value)
                setattr(args, DatabaseKeys.USE_VARS_OPTION, True)
            case _:
                if not getattr(args, DatabaseKeys.DB.value):
                    setattr(args, DatabaseKeys.DB, DatabaseOptions.SQLITE.value)

        if (
            getattr(args, DatabaseKeys.USE_VARS_OPTION.value)
            and getattr(args, DatabaseKeys.DB.value) != DatabaseOptions.POSTGRESQL.value
        ):
            raise ValueError(
                f"The --{DatabaseKeys.USE_VARS_OPTION.value} flag is only supported for {DatabaseOptions.POSTGRESQL.value}."
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
        api_dir = output_dir / "api"

        base_specs: dict[str, FileSpec] = {
            _GenerateTargets.API_INIT: FileSpec(
                path=api_dir / "__init__.py", content='"""API module."""'
            ),
            _GenerateTargets.API_SERVER: FileSpec(
                path=api_dir / "server.py", content=self._content_api_server_py()
            ),
            _GenerateTargets.GITIGNORE: FileSpec(
                path=output_dir / ".gitignore", content=self._content_gitignore(args)
            ),
            _GenerateTargets.PYPROJECT: FileSpec(
                path=output_dir / "pyproject.toml",
                content=self._content_pyproject_toml(project_name, args),
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
            _GenerateTargets.API_SERVER,
            _GenerateTargets.GITIGNORE,
            _GenerateTargets.PYPROJECT,
            _GenerateTargets.README,
            _GenerateTargets.CONFIG_MD,
        ]
        if getattr(args, PresetKeys.PRESET) == PresetOptions.VERCEL:
            ordered_targets.append(_GenerateTargets.VERCEL_JSON)

        return [base_specs[target_name] for target_name in ordered_targets]

    def _content_gitignore(self, args: Namespace) -> str:
        """Generate .gitignore content."""
        sqlite = (
            f"\n# SQLite database\n/db.{DatabaseOptions.SQLITE}3\n"
            if getattr(args, DatabaseKeys.DB) == DatabaseOptions.SQLITE
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
        allowed_hosts = ['"localhost"', '"127.0.0.1"']
        tool_lines = [f"[tool.{FETCH_PROJECT.pkg_name}]"]

        # ---------------------------------------------

        if is_vercel:
            extras.append(PresetOptions.VERCEL.value)
            allowed_hosts.append('".vercel.app"')
            tool_lines.append(
                f"{PresetKeys.PRESET} = {{ "
                f'{PresetKeys.OPTION} = "{PresetOptions.VERCEL}", '
                f'{PresetKeys.BLOB_TOKEN} = "{PresetDefaults.BLOB_TOKEN.value}" '
                "}"
            )
        elif uses_postgresql:
            extras.append(DatabaseOptions.POSTGRESQL.value)
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

        # ---------------------------------------------

        extras_suffix = f"[{','.join(extras)}]" if extras else ""
        dependencies = (
            f'"{FETCH_PROJECT.pkg_name}{extras_suffix}=={FETCH_PROJECT.pkg_version}"'
        )
        tool_section = "\n".join(tool_lines) + "\n"

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
            f"{tool_section}\n"
        )

    def _content_api_server_py(self) -> str:
        """Generate API server entry-point file content."""
        return f"from {API_PKG_MODULE}.sgi import application\n\napp = application\n"

    def _content_vercel_json(self) -> str:
        """Generate vercel.json content for Vercel preset."""
        lines = [
            "{",
            '  "$schema": "https://openapi.vercel.sh/vercel.json",',
            '  "framework": null,',
            f'  "installCommand": "uv run {FETCH_PROJECT.pkg_name} runinstall",',
            f'  "buildCommand": "uv run {FETCH_PROJECT.pkg_name} runbuild",',
            '  "rewrites": [',
            "    {",
            '      "source": "/(.*)",',
            '      "destination": "/api/server.py"',
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
            f"# {FETCH_PROJECT.pkg_display_name} Configuration Reference",
            "",
            f"A generated reference of all supported `tool.{FETCH_PROJECT.pkg_name}` settings, their defaults, and allowed values.",
            "",
            f"Generated on: {generated_on}",
            "",
            "## Source Priority",
            "",
            "Configuration is resolved in this order:",
            "1. Environment variables",
            f"2. `pyproject.toml` in `[tool.{FETCH_PROJECT.pkg_name}]` section",
            "3. Schema defaults",
            "",
        ]

        sections: list[tuple[str, dict[str, Any]]] = [
            ("Security & Deployment", SECURITY_SCHEMA),
            ("Presets & Storages", PRESET_SCHEMA),
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
