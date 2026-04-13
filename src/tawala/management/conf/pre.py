"""Pre-initialization Configurations."""

import builtins
import pathlib
from typing import Any, TypeAlias, cast

from ... import CONF
from .. import (
    ConfFieldKeys,
    DatabaseKeys,
    DatabaseOptions,
    InternationalizationKeys,
    PresetKeys,
    PresetOptions,
    RuncommandKeys,
    SecurityKeys,
)
from .mappings import (
    DATABASES_CONF_MAPPING,
    INTERNATIONALIZATION_CONF_MAPPING,
    PRESETS_CONF_MAPPING,
    RUNCOMMANDS_CONF_MAPPING,
    SECURITY_CONF_MAPPING,
)

_ConfDefaultValueType: TypeAlias = str | bool | list[str] | pathlib.Path | int | None


class _ConfField:
    """Descriptor for a configuration field populated from env vars or TOML."""

    def __init__(
        self,
        type: type[str]
        | type[bool]
        | type[list[str]]
        | type[pathlib.Path]
        | type[int] = str,
        choices: list[str] | None = None,
        env: str | None = None,
        toml: str | None = None,
        default: _ConfDefaultValueType = None,
    ):
        """Set up field type, source mappings, and default value."""
        self.type = type
        self.choices = choices
        self.env = env
        self.toml = toml
        self.default = default
        self.field_name: str = ""

    # ============================================================================
    # Value Resolution
    # ============================================================================

    def _get_from_toml(self) -> Any:
        """Get value from TOML configuration."""
        if self.toml is None:
            return None
        current: Any = CONF.base_toml
        for k in self.toml.split("."):
            if isinstance(current, dict) and k in current:
                current = cast(dict[str, Any], current)[k]
            else:
                return None
        return current

    def _fetch_value(self) -> Any:
        """Fetch configuration value with fallback priority: ENV -> TOML -> default."""
        if self.env is not None and self.env in CONF.base_env:
            return CONF.base_env[self.env]
        toml_value = self._get_from_toml()
        if toml_value is not None:
            return toml_value
        return self.default

    # ============================================================================
    # Value Conversion
    # ============================================================================

    @staticmethod
    def convert_value(
        value: Any, target_type: Any, field_name: str | None = None
    ) -> _ConfDefaultValueType:
        """Convert a raw value to the target type."""
        from christianwhocodes import TypeConverter

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
                    raise ValueError(
                        f"Unsupported target type or type not specified: {target_type}"
                    )
        except ValueError as e:
            field_info = f" for field '{field_name}'" if field_name else ""
            raise ValueError(f"Error converting config value{field_info}: {e}") from e

        raise ValueError(
            f"Unsupported target type or conversion failure for: {target_type}"
        )

    # ============================================================================
    # Descriptor Protocol
    # ============================================================================

    def __set_name__(self, owner: type, name: str) -> None:
        """Capture the attribute name when the descriptor is assigned to a class."""
        self.field_name = name

    def __get__(self, instance: Any, owner: type) -> Any:
        """Fetch, convert, and return the configuration value."""
        if instance is None:
            return self
        raw_value = self._fetch_value()
        return self.convert_value(raw_value, self.type, self.field_name)


def _build_conf_field(mapping: Any, field_name: str) -> _ConfField:
    """Build a config field from centralized metadata."""
    field_config = mapping[field_name]
    return _ConfField(
        type=field_config.get(ConfFieldKeys.TYPE),
        choices=field_config.get(ConfFieldKeys.CHOICES),
        env=field_config.get(ConfFieldKeys.ENV),
        toml=field_config.get(ConfFieldKeys.TOML),
        default=field_config.get(ConfFieldKeys.DEFAULT),
    )


# ============================================================================
# Core
# ============================================================================


class _BaseConf:
    """Core Configuration."""

    pkg_name = CONF.pkg_name
    pkg_display_name = CONF.pkg_display_name
    pkg_version = CONF.pkg_version
    base_dir = CONF.base_dir


BASE_CONF = _BaseConf()

# ============================================================================
# Presets & Storages
# ============================================================================


class _PresetsConf:
    """Presets and Storages Configuration."""

    backend = _build_conf_field(PRESETS_CONF_MAPPING, PresetKeys.BACKEND)
    blob_read_write_token = _build_conf_field(
        PRESETS_CONF_MAPPING, PresetKeys.BLOB_TOKEN
    )


PRESETS_CONF = _PresetsConf()


# ============================================================================
# Security
# ============================================================================


class _SecurityConf:
    """Security and Deployment Configuration."""

    secret_key = _build_conf_field(SECURITY_CONF_MAPPING, SecurityKeys.SECRET_KEY)
    debug = _build_conf_field(SECURITY_CONF_MAPPING, SecurityKeys.DEBUG)
    allowed_hosts = _build_conf_field(SECURITY_CONF_MAPPING, SecurityKeys.ALLOWED_HOSTS)
    secure_ssl_redirect = _build_conf_field(
        SECURITY_CONF_MAPPING, SecurityKeys.SECURE_SSL_REDIRECT
    )
    session_cookie_secure = _build_conf_field(
        SECURITY_CONF_MAPPING, SecurityKeys.SESSION_COOKIE_SECURE
    )
    csrf_cookie_secure = _build_conf_field(
        SECURITY_CONF_MAPPING, SecurityKeys.CSRF_COOKIE_SECURE
    )
    secure_hsts_seconds = _build_conf_field(
        SECURITY_CONF_MAPPING, SecurityKeys.SECURE_HSTS_SECONDS
    )
    work_in_progress = _build_conf_field(
        SECURITY_CONF_MAPPING, SecurityKeys.WORK_IN_PROGRESS
    )
    admin_enabled = _build_conf_field(SECURITY_CONF_MAPPING, SecurityKeys.ADMIN_ENABLED)


SECURITY_CONF = _SecurityConf()


# ============================================================================
# Databases
# ============================================================================


class _DatabasesConf:
    """Database Configuration."""

    # This check happens when the module is imported, so these are startup defaults.
    _is_vercel_preset = PRESETS_CONF.backend == PresetOptions.VERCEL
    # Start from a copy of the shared mapping so we can safely customize defaults for
    # this class without changing DATABASES_CONF_MAPPING for any other consumer.
    _field_mapping = {
        field_name: field_config.copy()
        for field_name, field_config in DATABASES_CONF_MAPPING.items()
    }
    # Only the fallback defaults are changed here. Runtime precedence is still:
    # environment variable -> pyproject.toml -> default.
    # Vercel preset defaults to PostgreSQL and enables variable-based PG settings.
    _field_mapping[DatabaseKeys.BACKEND][ConfFieldKeys.DEFAULT] = (
        DatabaseOptions.POSTGRESQL if _is_vercel_preset else DatabaseOptions.SQLITE
    )
    _field_mapping[DatabaseKeys.USE_VARS][ConfFieldKeys.DEFAULT] = _is_vercel_preset

    # Build each descriptor from the adjusted mapping so conversion and resolution
    # logic remains centralized in _build_conf_field/_ConfField.
    backend = _build_conf_field(_field_mapping, DatabaseKeys.BACKEND)
    # PostgreSQL connection fields (used when backend resolves to PostgreSQL).
    pg_use_vars = _build_conf_field(_field_mapping, DatabaseKeys.USE_VARS)
    pg_service = _build_conf_field(_field_mapping, DatabaseKeys.SERVICE)
    pg_user = _build_conf_field(_field_mapping, DatabaseKeys.USER)
    pg_password = _build_conf_field(_field_mapping, DatabaseKeys.PASSWORD)
    pg_database = _build_conf_field(_field_mapping, DatabaseKeys.NAME)
    pg_host = _build_conf_field(_field_mapping, DatabaseKeys.HOST)
    pg_port = _build_conf_field(_field_mapping, DatabaseKeys.PORT)
    pg_pool = _build_conf_field(_field_mapping, DatabaseKeys.POOL)
    pg_sslmode = _build_conf_field(_field_mapping, DatabaseKeys.SSLMODE)


DATABASES_CONF = _DatabasesConf()


# ============================================================================
# Internationalization
# ============================================================================


class _InternationalizationConf:
    """Internationalization Configuration."""

    language_code = _build_conf_field(
        INTERNATIONALIZATION_CONF_MAPPING, InternationalizationKeys.LANGUAGE_CODE
    )
    time_zone = _build_conf_field(
        INTERNATIONALIZATION_CONF_MAPPING, InternationalizationKeys.TIME_ZONE
    )
    use_i18n = _build_conf_field(
        INTERNATIONALIZATION_CONF_MAPPING, InternationalizationKeys.USE_I18N
    )
    use_tz = _build_conf_field(
        INTERNATIONALIZATION_CONF_MAPPING, InternationalizationKeys.USE_TZ
    )


INTERNATIONALIZATION_CONF = _InternationalizationConf()


# ============================================================================
# Runcommands
# ============================================================================


class _RunCommandsConf:
    """Runcommands Configuration."""

    install = _build_conf_field(RUNCOMMANDS_CONF_MAPPING, RuncommandKeys.INSTALL)
    build = _build_conf_field(RUNCOMMANDS_CONF_MAPPING, RuncommandKeys.BUILD)


RUNCOMMANDS_CONF = _RunCommandsConf()
