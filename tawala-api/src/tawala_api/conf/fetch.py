"""Settings conf."""

import builtins
import pathlib
from dataclasses import replace
from enum import Enum
from functools import cached_property
from typing import Any, Final, TypeAlias, cast

from christianwhocodes import PyProject, Version

from .enums import (
    DatabaseKeys,
    DatabaseOptions,
    InternationalizationKeys,
    LayoutKeys,
    PresetKeys,
    PresetOptions,
    RuncommandKeys,
    SecurityKeys,
)
from .mappings import (
    DATABASES_SCHEMA,
    INTERNATIONALIZATION_SCHEMA,
    LAYOUT_SCHEMA,
    PRESET_SCHEMA,
    RUNCOMMANDS_SCHEMA,
    SECURITY_SCHEMA,
    SchemaField,
)

# ============================================================================
# Module Exports
# ============================================================================
__all__ = [
    "FetchProjectValidationError",
    "FETCH_PROJECT",
    "FETCH_SECURITY",
    "FETCH_PRESET",
    "FETCH_DATABASES",
    "FETCH_LAYOUT",
    "FETCH_INTERNATIONALIZATION",
    "FETCH_RUNCOMMANDS",
]


class FetchProjectValidationError(Exception):
    """Raised when the root directory or config is invalid."""

    def __init__(
        self,
        message: str = "Current directory could not be loaded. Ensure the directory is a valid project directory.",
    ) -> None:
        """Initialize the validation error with a default message."""
        super().__init__(message)


# ============================================================================
# Root
# ============================================================================
class _FetchProject:
    """Root configuration."""

    def __init__(self) -> None:
        """Initialize project configuration for a specific package."""
        self._validated = False
        self._base_toml: dict[str, Any] = {}
        self._base_dir: pathlib.Path | None = None

        self.pkg_name: Final[str] = "tawala"
        self.pkg_display_name: Final[str] = self.pkg_name.capitalize()
        self.pkg_version: Final[str] = Version.get(self.pkg_name)[0]

        self.core_app = f"{self.pkg_name}.core"
        self.main_app = "app"

    def _load_project(self) -> None:
        """Load and validate pyproject.toml configuration."""
        pyproject_path = pathlib.Path.cwd() / "pyproject.toml"
        if not pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at '{pyproject_path}'")
        tool_section = PyProject(pyproject_path).data.get("tool", {})
        if self.pkg_name not in tool_section:
            raise KeyError(f"Missing 'tool.{self.pkg_name}' section in pyproject.toml")
        self._base_toml = tool_section[self.pkg_name]
        self._base_dir = pyproject_path.parent

    def validate_project(self) -> None:
        """Validate the project once; subsequent calls are no-ops."""
        if self._validated:
            return
        try:
            self._load_project()
        except (FileNotFoundError, KeyError) as e:
            raise FetchProjectValidationError(str(e)) from e
        self._validated = True

    @cached_property
    def base_toml(self) -> dict[str, Any]:
        """pyproject.toml config section for this package (lazy-loaded)."""
        self.validate_project()
        return self._base_toml

    @cached_property
    def base_dir(self) -> pathlib.Path:
        """Root directory containing pyproject.toml (lazy-loaded)."""
        self.validate_project()
        assert self._base_dir is not None  # guaranteed after validate()
        return self._base_dir

    @cached_property
    def base_env(self) -> dict[str, Any]:
        """Merged .env file and process environment variables (lazy-loaded)."""
        from os import environ

        from dotenv import dotenv_values

        return {**dotenv_values(self.base_dir / ".env"), **environ}

    # TODO: Has this been used anywhere? If not remove it.
    @cached_property
    def base_name(self) -> str:
        """Project name derived from the project directory name (lazy-loaded)."""
        return self.base_dir.name


FETCH_PROJECT = _FetchProject()
"""Singleton instance of configuration and validation utilities.

POLICY: Inisde the this package, only modules marked with "[FETCH_PROJECT_IMPORT_ALLOWED]"
in their module docstring should import FETCH_PROJECT/FetchProjectValidationError.
If any other module needs FETCH_PROJECT's functionality, use the ones set in
settings.py via `from django.conf import settings`
"""

# ============================================================================
# FetchField
# ============================================================================
_FetchValueDefault: TypeAlias = str | bool | list[str] | pathlib.Path | int | None


class _FetchField:
    """Descriptor for a configuration field populated from env vars or TOML."""

    def __init__(
        self,
        type: type[str]
        | type[bool]
        | type[list[str]]
        | type[pathlib.Path]
        | type[int] = str,
        options: list[str] | None = None,
        env: str | None = None,
        toml: str | None = None,
        default: _FetchValueDefault = None,
    ):
        """Set up field type, source mappings, and default value."""
        self.type = type
        self.env = env
        self.toml = toml
        self.default = default
        self.options = options
        self.field_name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Capture the attribute name when the descriptor is assigned to a class."""
        self.field_name = name

    def __get__(self, instance: Any, owner: type) -> Any:
        """Fetch, convert, and return the configuration value."""
        if instance is None:
            return self
        raw_value = self._fetch_value()
        return self.convert_value(raw_value, self.type, self.field_name)

    def _get_from_toml(self) -> Any:
        """Get value from TOML configuration."""
        if self.toml is None:
            return None
        try:
            current: Any = FETCH_PROJECT.base_toml
        except FetchProjectValidationError:
            # NOTE: Descriptors can also be touched at import
            # time while class-body defaults are being computed. If validation is
            # unavailable in that phase, continue. API entry modules (cli.py,
            # asgi.py, wsgi.py) should perform project validation first, and
            # _ConfField should not be responsible for surfacing that error.
            return None
        for k in self.toml.split("."):
            if isinstance(current, dict) and k in current:
                current = cast(dict[str, Any], current)[k]
            else:
                return None
        return current

    def _fetch_value(self) -> Any:
        """Fetch configuration value with fallback priority: ENV -> TOML -> default."""
        if self.env is not None:
            try:
                if self.env in FETCH_PROJECT.base_env:
                    return FETCH_PROJECT.base_env[self.env]
            except FetchProjectValidationError:
                # NOTE: Descriptors can also be touched at import
                # time while class-body defaults are being computed. If validation is
                # unavailable in that phase, continue. API entry modules (cli.py,
                # asgi.py, wsgi.py) should perform project validation first, and
                # _ConfField should not be responsible for surfacing that error.
                pass
        toml_value = self._get_from_toml()
        if toml_value is not None:
            return toml_value
        return self.default

    @staticmethod
    def convert_value(
        value: Any, target_type: Any, field_name: str | None = None
    ) -> _FetchValueDefault:
        """Convert a raw value to the target type."""
        from christianwhocodes import TypeConverter

        if isinstance(value, Enum):
            value = value.value

        if value is None:
            match target_type:
                case builtins.str:
                    return ""
                case builtins.int:
                    return 0
                case builtins.list:
                    return []
                case _:
                    return None
        try:
            match target_type:
                case builtins.str:
                    return str(value)
                case builtins.int:
                    return int(value)
                case builtins.list:
                    return TypeConverter.to_list_of_str(value, str.strip)
                case builtins.bool:
                    return TypeConverter.to_bool(value)
                case pathlib.Path:
                    return TypeConverter.to_path(value)
                case _:
                    pass
        except ValueError as e:
            field_info = f" for field '{field_name}'" if field_name else ""
            raise ValueError(f"Error converting config value{field_info}: {e}") from e

        raise ValueError(
            f"Unsupported target type or conversion failure for: {target_type}"
        )


def _build_fetch_field(schema: dict[str, SchemaField], field_name: str) -> _FetchField:
    """Build a config field from centralized metadata."""
    field_config = schema[field_name]
    return _FetchField(
        type=field_config.type,
        env=field_config.env,
        toml=field_config.toml,
        default=field_config.default,
        options=field_config.options,
    )


# ============================================================================
# Security & Deployment
# ============================================================================
class _FetchSecurity:
    """Security and Deployment Configuration."""

    secret_key = _build_fetch_field(SECURITY_SCHEMA, SecurityKeys.SECRET_KEY)
    debug_option = _build_fetch_field(SECURITY_SCHEMA, SecurityKeys.DEBUG_OPTION)
    allowed_hosts = _build_fetch_field(SECURITY_SCHEMA, SecurityKeys.ALLOWED_HOSTS)
    secure_ssl_redirect = _build_fetch_field(
        SECURITY_SCHEMA, SecurityKeys.SECURE_SSL_REDIRECT_OPTION
    )
    session_cookie_secure = _build_fetch_field(
        SECURITY_SCHEMA, SecurityKeys.SESSION_COOKIE_SECURE_OPTION
    )
    csrf_cookie_secure = _build_fetch_field(
        SECURITY_SCHEMA, SecurityKeys.CSRF_COOKIE_SECURE_OPTION
    )
    secure_hsts_seconds = _build_fetch_field(
        SECURITY_SCHEMA, SecurityKeys.SECURE_HSTS_SECONDS
    )


FETCH_SECURITY = _FetchSecurity()


# ============================================================================
# Presets & Storages
# NOTE: Must be defined before _FetchDatabases and _FetchLayout — its backend value is read at
# class body evaluation time to set database defaults.
# ============================================================================
class _FetchPreset:
    """Presets and Storages Configuration."""

    option = _build_fetch_field(PRESET_SCHEMA, PresetKeys.OPTION)
    blob_read_write_token = _build_fetch_field(PRESET_SCHEMA, PresetKeys.BLOB_TOKEN)


FETCH_PRESET = _FetchPreset()


# ============================================================================
# Databases
# NOTE: Must be defined after _FetchPreset since it reads the preset backend value.
# ============================================================================
class _FetchDatabases:
    """Database Configuration."""

    _is_vercel_preset = FETCH_PRESET.option == PresetOptions.VERCEL
    # Start from a copy so the shared schema stays unchanged for other consumers.
    _field_schema = {
        field_name: replace(field_config)
        for field_name, field_config in DATABASES_SCHEMA.items()
    }
    # Only the fallback defaults are changed here. Runtime precedence is still:
    # environment variable -> pyproject.toml -> default.
    # Vercel preset defaults to PostgreSQL and enables variable-based PG settings.
    _field_schema[DatabaseKeys.OPTION] = replace(
        _field_schema[DatabaseKeys.OPTION],
        default=(
            DatabaseOptions.POSTGRESQL if _is_vercel_preset else DatabaseOptions.SQLITE
        ),
    )
    _field_schema[DatabaseKeys.USE_VARS_OPTION] = replace(
        _field_schema[DatabaseKeys.USE_VARS_OPTION],
        default=_is_vercel_preset,
    )

    option = _build_fetch_field(_field_schema, DatabaseKeys.OPTION)
    # PostgreSQL connection fields (used when backend resolves to PostgreSQL).
    pg_use_vars = _build_fetch_field(_field_schema, DatabaseKeys.USE_VARS_OPTION)
    pg_service = _build_fetch_field(_field_schema, DatabaseKeys.SERVICE)
    pg_user = _build_fetch_field(_field_schema, DatabaseKeys.USER)
    pg_password = _build_fetch_field(_field_schema, DatabaseKeys.PASSWORD)
    pg_database = _build_fetch_field(_field_schema, DatabaseKeys.NAME)
    pg_host = _build_fetch_field(_field_schema, DatabaseKeys.HOST)
    pg_port = _build_fetch_field(_field_schema, DatabaseKeys.PORT)
    pg_pool = _build_fetch_field(_field_schema, DatabaseKeys.POOL_OPTION)
    pg_sslmode = _build_fetch_field(_field_schema, DatabaseKeys.SSLMODE_OPTION)


FETCH_DATABASES = _FetchDatabases()


# ============================================================================
# Layout
# NOTE: Must be defined after _FetchPreset since it reads the preset backend value.
# ============================================================================
class _FetchLayout:
    """Layout Configuration."""

    # Start from a copy so the shared schema stays unchanged for other consumers.
    _field_schema = {
        field_name: replace(field_config)
        for field_name, field_config in LAYOUT_SCHEMA.items()
    }
    # The fallback default is resolved at import time from the security config.
    _field_schema[LayoutKeys.ALWAYS_SHOW_ADMIN_OPTION] = replace(
        _field_schema[LayoutKeys.ALWAYS_SHOW_ADMIN_OPTION],
        default=FETCH_SECURITY.debug_option,
    )

    option = _build_fetch_field(_field_schema, LayoutKeys.OPTION)
    always_show_admin = _build_fetch_field(
        _field_schema, LayoutKeys.ALWAYS_SHOW_ADMIN_OPTION
    )


FETCH_LAYOUT = _FetchLayout()


# ============================================================================
# Internationalization
# ============================================================================
class _FetchInternationalization:
    """Internationalization Configuration."""

    language_code = _build_fetch_field(
        INTERNATIONALIZATION_SCHEMA, InternationalizationKeys.LANGUAGE_CODE
    )
    time_zone = _build_fetch_field(
        INTERNATIONALIZATION_SCHEMA, InternationalizationKeys.TIME_ZONE
    )
    use_i18n = _build_fetch_field(
        INTERNATIONALIZATION_SCHEMA, InternationalizationKeys.USE_I18N
    )
    use_tz = _build_fetch_field(
        INTERNATIONALIZATION_SCHEMA, InternationalizationKeys.USE_TZ
    )


FETCH_INTERNATIONALIZATION = _FetchInternationalization()


# ============================================================================
# Runcommands
# ============================================================================
class _FetchRuncommands:
    """Runcommands Configuration."""

    install = _build_fetch_field(RUNCOMMANDS_SCHEMA, RuncommandKeys.INSTALL)
    build = _build_fetch_field(RUNCOMMANDS_SCHEMA, RuncommandKeys.BUILD)


FETCH_RUNCOMMANDS = _FetchRuncommands()
