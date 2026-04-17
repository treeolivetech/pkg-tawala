"""Settings schema."""

from dataclasses import dataclass, field
from typing import Any, TypeAlias, cast

from .enums import (
    DatabaseKeys,
    DatabaseOptions,
    DatabasePoolOptions,
    DatabaseSSlModeOptions,
    DatabaseUseVarsOptions,
    InternationalizationKeys,
    LayoutAlwaysShowAdminOptions,
    LayoutKeys,
    LayoutOptions,
    PresetBlobTokenDefaults,
    PresetKeys,
    PresetOptions,
    RuncommandKeys,
    SecurityAllowedHostsDefaults,
    SecurityDebugOptions,
    SecurityKeys,
)


@dataclass(frozen=True)
class SchemaField:
    """Definition for a single configurable field in the settings schema."""

    type: type[Any]
    env: str
    toml: str
    default: Any
    options: list[Any] = field(default_factory=lambda: cast(list[Any], []))
    help_text: str = ""


_Schema: TypeAlias = dict[str, SchemaField]

# ============================================================================
# Module Exports
# ============================================================================
__all__ = [
    "SECURITY_SCHEMA",
    "PRESETS_SCHEMA",
    "DATABASES_SCHEMA",
    "LAYOUT_SCHEMA",
    "INTERNATIONALIZATION_SCHEMA",
    "RUNCOMMANDS_SCHEMA",
]

# ============================================================================
# Security & Deployment
# ============================================================================
SECURITY_SCHEMA: _Schema = {
    SecurityKeys.SECRET_KEY: SchemaField(
        type=str,
        env="SECRET_KEY",
        toml=SecurityKeys.SECRET_KEY,
        default="django-insecure-change-me-in-production-via-env-variable",
        help_text="Secret key used for cryptographic signing. Always set this in production.",
    ),
    SecurityKeys.DEBUG_OPTION: SchemaField(
        type=bool,
        env="DEBUG_OPTION",
        toml=SecurityKeys.DEBUG_OPTION,
        default=SecurityDebugOptions.DEFAULT_ENABLED,
        options=list(SecurityDebugOptions),
        help_text="Enable debug mode. Keep disabled in production environments.",
    ),
    SecurityKeys.ALLOWED_HOSTS: SchemaField(
        type=list,
        env="ALLOWED_HOSTS",
        toml=SecurityKeys.ALLOWED_HOSTS,
        default=list(SecurityAllowedHostsDefaults),
        help_text="List of hostnames the app is allowed to serve.",
    ),
    SecurityKeys.SECURE_SSL_REDIRECT: SchemaField(
        type=bool,
        env="SECURE_SSL_REDIRECT",
        toml=SecurityKeys.SECURE_SSL_REDIRECT,
        default=False,
        help_text="Redirect all HTTP requests to HTTPS when enabled.",
    ),
    SecurityKeys.SESSION_COOKIE_SECURE: SchemaField(
        type=bool,
        env="SESSION_COOKIE_SECURE",
        toml=SecurityKeys.SESSION_COOKIE_SECURE,
        default=False,
        help_text="Mark session cookies as secure so they are sent only over HTTPS.",
    ),
    SecurityKeys.CSRF_COOKIE_SECURE: SchemaField(
        type=bool,
        env="CSRF_COOKIE_SECURE",
        toml=SecurityKeys.CSRF_COOKIE_SECURE,
        default=False,
        help_text="Mark CSRF cookies as secure so they are sent only over HTTPS.",
    ),
    SecurityKeys.SECURE_HSTS_SECONDS: SchemaField(
        type=int,
        env="SECURE_HSTS_SECONDS",
        toml=SecurityKeys.SECURE_HSTS_SECONDS,
        default=0,
        help_text="HTTP Strict Transport Security max-age value in seconds.",
    ),
}


# ============================================================================
# Presets & Storages
# ============================================================================
PRESETS_SCHEMA: _Schema = {
    PresetKeys.OPTION: SchemaField(
        type=str,
        env="PRESET_OPTION",
        toml=f"{PresetKeys.PRESET}.{PresetKeys.OPTION}",
        default=PresetOptions.DEFAULT,
        options=list(PresetOptions),
        help_text="Deployment preset that controls opinionated defaults for the project.",
    ),
    PresetKeys.BLOB_TOKEN: SchemaField(
        type=str,
        env="BLOB_READ_WRITE_TOKEN",
        toml=f"{PresetKeys.PRESET}.{PresetKeys.BLOB_TOKEN}",
        default=PresetBlobTokenDefaults.GET_FROM_VERCEL,
        help_text="Token used for blob storage read/write access when blob support is enabled.",
    ),
}


# ============================================================================
# Databases
# ============================================================================
DATABASES_SCHEMA: _Schema = {
    DatabaseKeys.OPTION: SchemaField(
        type=str,
        env="DB_OPTION",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.OPTION}",
        default=DatabaseOptions.DEFAULT_SQLITE,
        options=list(DatabaseOptions),
        help_text="Database backend to use, such as SQLite or PostgreSQL.",
    ),
    DatabaseKeys.USE_VARS_OPTION: SchemaField(
        type=bool,
        env="DB_USE_VARS_OPTION",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.USE_VARS_OPTION}",
        default=DatabaseUseVarsOptions.DEFAULT_DISABLED,
        options=list(DatabaseUseVarsOptions),
        help_text="Enable reading PostgreSQL connection values from individual DB_* variables.",
    ),
    DatabaseKeys.SERVICE: SchemaField(
        type=str,
        env="DB_PGSERVICE",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.SERVICE}",
        default="",
        help_text="PostgreSQL service name from pg_service.conf, if used.",
    ),
    DatabaseKeys.USER: SchemaField(
        type=str,
        env="DB_PGUSER",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.USER}",
        default="",
        help_text="PostgreSQL username for database authentication.",
    ),
    DatabaseKeys.PASSWORD: SchemaField(
        type=str,
        env="DB_PGPASSWORD",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.PASSWORD}",
        default="",
        help_text="PostgreSQL password for database authentication.",
    ),
    DatabaseKeys.NAME: SchemaField(
        type=str,
        env="DB_PGDATABASE",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.NAME}",
        default="",
        help_text="PostgreSQL database name to connect to.",
    ),
    DatabaseKeys.HOST: SchemaField(
        type=str,
        env="DB_PGHOST",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.HOST}",
        default="",
        help_text="PostgreSQL host or socket location.",
    ),
    DatabaseKeys.PORT: SchemaField(
        type=int,
        env="DB_PGPORT",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.PORT}",
        default=5432,
        help_text="PostgreSQL server port.",
    ),
    DatabaseKeys.POOL_OPTION: SchemaField(
        type=bool,
        env="DB_PGPOOL_OPTION",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.POOL_OPTION}",
        default=DatabasePoolOptions.DEFAULT_DISABLED,
        options=list(DatabasePoolOptions),
        help_text="Enable PostgreSQL connection pooling when supported.",
    ),
    DatabaseKeys.SSLMODE_OPTION: SchemaField(
        type=str,
        env="DB_PGSSLMODE_OPTION",
        toml=f"{DatabaseKeys.DB}.{DatabaseKeys.SSLMODE_OPTION}",
        default=DatabaseSSlModeOptions.DEFAULT_PREFER,
        options=list(DatabaseSSlModeOptions),
        help_text="PostgreSQL SSL mode for transport security.",
    ),
}


# ============================================================================
# Layout
# ============================================================================
LAYOUT_SCHEMA: _Schema = {
    LayoutKeys.OPTION: SchemaField(
        type=str,
        env="LAYOUT_OPTION",
        toml=f"{LayoutKeys.LAYOUT}.{LayoutKeys.OPTION}",
        default=LayoutOptions.DEFAULT_BASE,
        options=list(LayoutOptions),
        help_text="Primary layout template option used by the app.",
    ),
    LayoutKeys.ALWAYS_SHOW_ADMIN_OPTION: SchemaField(
        type=bool,
        env="LAYOUT_ALWAYS_SHOW_ADMIN_OPTION",
        toml=f"{LayoutKeys.LAYOUT}.{LayoutKeys.ALWAYS_SHOW_ADMIN_OPTION}",
        default=LayoutAlwaysShowAdminOptions.DEFAULT_DISABLED,
        options=list(LayoutAlwaysShowAdminOptions),
        help_text="Force admin links to display regardless of debug context.",
    ),
}


# ============================================================================
# Internationalization
# ============================================================================
INTERNATIONALIZATION_SCHEMA: _Schema = {
    InternationalizationKeys.LANGUAGE_CODE: SchemaField(
        type=str,
        env="LANGUAGE_CODE",
        toml=f"{InternationalizationKeys.INTERNATIONALIZATION}.{InternationalizationKeys.LANGUAGE_CODE}",
        default="en-us",
        help_text="Default language code used for internationalization.",
    ),
    InternationalizationKeys.TIME_ZONE: SchemaField(
        type=str,
        env="TIME_ZONE",
        toml=f"{InternationalizationKeys.INTERNATIONALIZATION}.{InternationalizationKeys.TIME_ZONE}",
        default="UTC",
        help_text="Default time zone used for date/time handling.",
    ),
    InternationalizationKeys.USE_I18N: SchemaField(
        type=bool,
        env="USE_I18N",
        toml=f"{InternationalizationKeys.INTERNATIONALIZATION}.{InternationalizationKeys.USE_I18N}",
        default=True,
        help_text="Enable translation and locale machinery.",
    ),
    InternationalizationKeys.USE_TZ: SchemaField(
        type=bool,
        env="USE_TZ",
        toml=f"{InternationalizationKeys.INTERNATIONALIZATION}.{InternationalizationKeys.USE_TZ}",
        default=True,
        help_text="Store and handle datetimes as timezone-aware values.",
    ),
}


# ============================================================================
# Runcommands
# ============================================================================
RUNCOMMANDS_SCHEMA: _Schema = {
    RuncommandKeys.INSTALL: SchemaField(
        type=list,
        env="RUNCOMMANDS_INSTALL",
        toml=f"{RuncommandKeys.RUNCOMMANDS}.{RuncommandKeys.INSTALL}",
        default=[],
        help_text="Management commands to run during project install/bootstrap.",
    ),
    RuncommandKeys.BUILD: SchemaField(
        type=list,
        env="RUNCOMMANDS_BUILD",
        toml=f"{RuncommandKeys.RUNCOMMANDS}.{RuncommandKeys.BUILD}",
        default=[
            "makemigrations",
            "migrate",
            "compilescss",
            "collectstatic --noinput --ignore=*.scss",
        ],
        help_text="Management commands to run during build/deploy preparation.",
    ),
}
