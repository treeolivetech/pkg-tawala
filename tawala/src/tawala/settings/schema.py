"""Settings schema."""

from typing import Any, TypeAlias

from .enums import (
    ConfFieldKeys,
    DatabaseKeys,
    DatabaseOptions,
    DatabasePoolOptions,
    DatabaseSSlModeOptions,
    DatabaseUseVarsOptions,
    InternationalizationKeys,
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

_MappingType: TypeAlias = dict[str, dict[str, Any]]

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
SECURITY_SCHEMA: _MappingType = {
    SecurityKeys.SECRET_KEY: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "SECRET_KEY",
        ConfFieldKeys.TOML: SecurityKeys.SECRET_KEY,
        ConfFieldKeys.DEFAULT: "django-insecure-change-me-in-production-via-env-variable",
    },
    SecurityKeys.DEBUG: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "DEBUG",
        ConfFieldKeys.TOML: SecurityKeys.DEBUG,
        ConfFieldKeys.DEFAULT: SecurityDebugOptions.DEFAULT_ENABLED,
        ConfFieldKeys.OPTIONS: list(SecurityDebugOptions),
    },
    SecurityKeys.ALLOWED_HOSTS: {
        ConfFieldKeys.TYPE: list,
        ConfFieldKeys.ENV: "ALLOWED_HOSTS",
        ConfFieldKeys.TOML: SecurityKeys.ALLOWED_HOSTS,
        ConfFieldKeys.DEFAULT: list(SecurityAllowedHostsDefaults),
    },
    SecurityKeys.SECURE_SSL_REDIRECT: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "SECURE_SSL_REDIRECT",
        ConfFieldKeys.TOML: SecurityKeys.SECURE_SSL_REDIRECT,
        ConfFieldKeys.DEFAULT: False,
    },
    SecurityKeys.SESSION_COOKIE_SECURE: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "SESSION_COOKIE_SECURE",
        ConfFieldKeys.TOML: SecurityKeys.SESSION_COOKIE_SECURE,
        ConfFieldKeys.DEFAULT: False,
    },
    SecurityKeys.CSRF_COOKIE_SECURE: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "CSRF_COOKIE_SECURE",
        ConfFieldKeys.TOML: SecurityKeys.CSRF_COOKIE_SECURE,
        ConfFieldKeys.DEFAULT: False,
    },
    SecurityKeys.SECURE_HSTS_SECONDS: {
        ConfFieldKeys.TYPE: int,
        ConfFieldKeys.ENV: "SECURE_HSTS_SECONDS",
        ConfFieldKeys.TOML: SecurityKeys.SECURE_HSTS_SECONDS,
        ConfFieldKeys.DEFAULT: 0,
    },
}


# ============================================================================
# Presets & Storages
# ============================================================================
PRESETS_SCHEMA: _MappingType = {
    PresetKeys.BACKEND: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "PRESET_BACKEND",
        ConfFieldKeys.TOML: f"{PresetKeys.PRESET}.{PresetKeys.BACKEND}",
        ConfFieldKeys.DEFAULT: PresetOptions.DEFAULT,
        ConfFieldKeys.OPTIONS: list(PresetOptions),
    },
    PresetKeys.BLOB_TOKEN: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "BLOB_READ_WRITE_TOKEN",
        ConfFieldKeys.TOML: f"{PresetKeys.PRESET}.{PresetKeys.BLOB_TOKEN}",
        ConfFieldKeys.DEFAULT: PresetBlobTokenDefaults.GET_FROM_VERCEL,
    },
}


# ============================================================================
# Databases
# ============================================================================
DATABASES_SCHEMA: _MappingType = {
    DatabaseKeys.BACKEND: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "DB_BACKEND",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.BACKEND}",
        ConfFieldKeys.DEFAULT: DatabaseOptions.DEFAULT_SQLITE,
        ConfFieldKeys.OPTIONS: list(DatabaseOptions),
    },
    DatabaseKeys.USE_VARS: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "DB_USE_VARS",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.USE_VARS}",
        ConfFieldKeys.DEFAULT: DatabaseUseVarsOptions.DEFAULT_DISABLED,
        ConfFieldKeys.OPTIONS: list(DatabaseUseVarsOptions),
    },
    DatabaseKeys.SERVICE: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "DB_PGSERVICE",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.SERVICE}",
        ConfFieldKeys.DEFAULT: "",
    },
    DatabaseKeys.USER: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "DB_PGUSER",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.USER}",
        ConfFieldKeys.DEFAULT: "",
    },
    DatabaseKeys.PASSWORD: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "DB_PGPASSWORD",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.PASSWORD}",
        ConfFieldKeys.DEFAULT: "",
    },
    DatabaseKeys.NAME: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "DB_PGDATABASE",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.NAME}",
        ConfFieldKeys.DEFAULT: "",
    },
    DatabaseKeys.HOST: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "DB_PGHOST",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.HOST}",
        ConfFieldKeys.DEFAULT: "",
    },
    DatabaseKeys.PORT: {
        ConfFieldKeys.TYPE: int,
        ConfFieldKeys.ENV: "DB_PGPORT",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.PORT}",
        ConfFieldKeys.DEFAULT: 5432,
    },
    DatabaseKeys.POOL: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "DB_PGPOOL",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.POOL}",
        ConfFieldKeys.DEFAULT: DatabasePoolOptions.DEFAULT_DISABLED,
        ConfFieldKeys.OPTIONS: list(DatabasePoolOptions),
    },
    DatabaseKeys.SSLMODE: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "DB_PGSSLMODE",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.SSLMODE}",
        ConfFieldKeys.DEFAULT: DatabaseSSlModeOptions.DEFAULT_PREFER,
        ConfFieldKeys.OPTIONS: list(DatabaseSSlModeOptions),
    },
}


# ============================================================================
# Layout
# ============================================================================
LAYOUT_SCHEMA: _MappingType = {
    LayoutKeys.BACKEND: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "LAYOUT_ORG",
        ConfFieldKeys.TOML: f"{LayoutKeys.LAYOUT}.{LayoutKeys.BACKEND}",
        ConfFieldKeys.DEFAULT: LayoutOptions.DEFAULT_BASE,
        ConfFieldKeys.OPTIONS: list(LayoutOptions),
    },
    LayoutKeys.ALWAYS_SHOW_ADMIN: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "LAYOUT_ALWAYS_SHOW_ADMIN",
        ConfFieldKeys.TOML: f"{LayoutKeys.LAYOUT}.{LayoutKeys.ALWAYS_SHOW_ADMIN}",
        # NOTE: Default set based on debug value in conf.py
    },
}


# ============================================================================
# Internationalization
# ============================================================================
INTERNATIONALIZATION_SCHEMA: _MappingType = {
    InternationalizationKeys.LANGUAGE_CODE: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "LANGUAGE_CODE",
        ConfFieldKeys.TOML: f"{InternationalizationKeys.INTERNATIONALIZATION}.{InternationalizationKeys.LANGUAGE_CODE}",
        ConfFieldKeys.DEFAULT: "en-us",
    },
    InternationalizationKeys.TIME_ZONE: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "TIMEZONE",
        ConfFieldKeys.TOML: f"{InternationalizationKeys.INTERNATIONALIZATION}.{InternationalizationKeys.TIME_ZONE}",
        ConfFieldKeys.DEFAULT: "UTC",
    },
    InternationalizationKeys.USE_I18N: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "USE_I18N",
        ConfFieldKeys.TOML: f"{InternationalizationKeys.INTERNATIONALIZATION}.{InternationalizationKeys.USE_I18N}",
        ConfFieldKeys.DEFAULT: True,
    },
    InternationalizationKeys.USE_TZ: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "USE_TZ",
        ConfFieldKeys.TOML: f"{InternationalizationKeys.INTERNATIONALIZATION}.{InternationalizationKeys.USE_TZ}",
        ConfFieldKeys.DEFAULT: True,
    },
}


# ============================================================================
# Runcommands
# ============================================================================
RUNCOMMANDS_SCHEMA: _MappingType = {
    RuncommandKeys.INSTALL: {
        ConfFieldKeys.TYPE: list,
        ConfFieldKeys.ENV: "RUNCOMMANDS_INSTALL",
        ConfFieldKeys.TOML: f"{RuncommandKeys.RUNCOMMANDS}.{RuncommandKeys.INSTALL}",
        ConfFieldKeys.DEFAULT: [],
    },
    RuncommandKeys.BUILD: {
        ConfFieldKeys.TYPE: list,
        ConfFieldKeys.ENV: "RUNCOMMANDS_BUILD",
        ConfFieldKeys.TOML: f"{RuncommandKeys.RUNCOMMANDS}.{RuncommandKeys.BUILD}",
        ConfFieldKeys.DEFAULT: [
            "makemigrations",
            "migrate",
            "compilescss",
            "collectstatic --noinput --ignore=*.scss",
        ],
    },
}
