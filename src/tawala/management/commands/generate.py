"""Management command for generating configuration files."""

from collections.abc import Callable
from enum import StrEnum
from pathlib import Path
from typing import Any, cast

from christianwhocodes import FileGenerator, FileSpec, get_pg_service_spec, get_pgpass_spec
from django.core.management.base import BaseCommand, CommandParser

from ... import PROJECT, Package


class _FileGenerateChoices(StrEnum):
    """Available file generation options."""

    README = "readme"
    APP_PY = "app_py"
    VERCEL_JSON = "vercel_json"
    PG_SERVICE = "pg_service"
    PGPASS = "pgpass"


def app_py_spec(path: Path = PROJECT.base_dir / "app.py") -> FileSpec:
    """Return the FileSpec for app.py."""
    content = f"from {Package.MAIN_APP} import asgi_application as application\n\napp = application\n"
    return FileSpec(path=path, content=content)


def vercel_json_spec(path: Path = PROJECT.base_dir / "vercel.json") -> FileSpec:
    """Return the FileSpec for vercel.json."""
    lines = [
        "{",
        '  "$schema": "https://openapi.vercel.sh/vercel.json",',
        '  "framework": "django",',
        f'  "installCommand": "uv run {Package.NAME} runinstall",',
        f'  "buildCommand": "uv run {Package.NAME} runbuild"',
        "}",
    ]
    return FileSpec(path=path, content="\n".join(lines) + "\n")


def readme_spec(path: Path = PROJECT.base_dir / "README.md") -> FileSpec:
    """Return the FileSpec for README.md with configuration documentation."""
    from ..settings import CONF_FIELDS
    from .helpers.readme import (
        readme_footer,
        readme_header,
        readme_section_header,
        readme_table_header,
        readme_table_row,
    )

    lines: list[str] = []
    lines.extend(readme_header(path.parent.name))  # Add header

    # Group fields by class
    fields_by_class: dict[str, list[dict[str, Any]]] = {}
    for field in CONF_FIELDS:
        class_name = cast(str, field["class"])
        if class_name not in fields_by_class:
            fields_by_class[class_name] = []
        fields_by_class[class_name].append(field)

    # Generate content for each class group
    for class_name in sorted(fields_by_class.keys()):
        fields = fields_by_class[class_name]
        lines.extend(readme_section_header(class_name))  # Add section header
        lines.extend(readme_table_header())  # Add table header

        # Process each field in this class
        for field in fields:
            env_var = field["env"]
            toml_key = field["toml"]
            choices_key = field["choices"]
            default_value = field["default"]
            field_type = field["type"]
            lines.append(readme_table_row(env_var, toml_key, choices_key, default_value, field_type))
        lines.append("")

    lines.extend(readme_footer())  # Add footer
    return FileSpec(path=path, content="\n".join(lines))


class Command(BaseCommand):
    """Generate configuration files."""

    help = "Generate configuration files."

    def add_arguments(self, parser: CommandParser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "file",
            choices=[opt for opt in _FileGenerateChoices],
            type=_FileGenerateChoices,
            help=f"Which file to generate (options: {', '.join(o for o in _FileGenerateChoices)}).",
        )
        parser.add_argument(
            "-f", "--force", dest="force", action="store_true", help="Force overwrite without confirmation."
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the generate command."""
        file_option = _FileGenerateChoices(options["file"])
        force: bool = options["force"]

        generators: dict[_FileGenerateChoices, Callable[[], FileSpec]] = {
            _FileGenerateChoices.README: readme_spec,
            _FileGenerateChoices.APP_PY: app_py_spec,
            _FileGenerateChoices.VERCEL_JSON: vercel_json_spec,
            _FileGenerateChoices.PG_SERVICE: get_pg_service_spec,
            _FileGenerateChoices.PGPASS: get_pgpass_spec,
        }

        spec: FileSpec = generators[file_option]()
        generator = FileGenerator(spec)
        generator.create(overwrite=force)
