"""Configuration mappings."""

from typing import Any, TypeAlias

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

_MappingType: TypeAlias = dict[str, dict[str, Any]]

PRESETS_CONF_MAPPING: _MappingType = {
    PresetKeys.BACKEND: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.CHOICES: [PresetOptions.DEFAULT, PresetOptions.VERCEL],
        ConfFieldKeys.ENV: "PRESET_BACKEND",
        ConfFieldKeys.TOML: f"{PresetKeys.PRESET}.{PresetKeys.BACKEND}",
        ConfFieldKeys.DEFAULT: PresetOptions.DEFAULT,
    },
    PresetKeys.BLOB_TOKEN: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.ENV: "BLOB_READ_WRITE_TOKEN",
        ConfFieldKeys.TOML: f"{PresetKeys.PRESET}.{PresetKeys.BLOB_TOKEN}",
        ConfFieldKeys.DEFAULT: "",
    },
}

SECURITY_CONF_MAPPING: _MappingType = {
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
        ConfFieldKeys.DEFAULT: True,
    },
    SecurityKeys.ALLOWED_HOSTS: {
        ConfFieldKeys.TYPE: list,
        ConfFieldKeys.ENV: "ALLOWED_HOSTS",
        ConfFieldKeys.TOML: SecurityKeys.ALLOWED_HOSTS,
        ConfFieldKeys.DEFAULT: ["localhost", "127.0.0.1"],
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
    SecurityKeys.WORK_IN_PROGRESS: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "WORK_IN_PROGRESS",
        ConfFieldKeys.TOML: SecurityKeys.WORK_IN_PROGRESS,
        ConfFieldKeys.DEFAULT: False,
    },
    SecurityKeys.ADMIN_ENABLED: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "ADMIN_ENABLED",
        ConfFieldKeys.TOML: SecurityKeys.ADMIN_ENABLED,
        ConfFieldKeys.DEFAULT: False,
    },
}

DATABASES_CONF_MAPPING: _MappingType = {
    DatabaseKeys.BACKEND: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.CHOICES: list(DatabaseOptions),
        ConfFieldKeys.ENV: "DB_BACKEND",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.BACKEND}",
        ConfFieldKeys.DEFAULT: DatabaseOptions.SQLITE,
    },
    DatabaseKeys.USE_VARS: {
        ConfFieldKeys.TYPE: bool,
        ConfFieldKeys.ENV: "DB_USE_VARS",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.USE_VARS}",
        ConfFieldKeys.DEFAULT: False,
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
        ConfFieldKeys.DEFAULT: "localhost",
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
        ConfFieldKeys.DEFAULT: False,
    },
    DatabaseKeys.SSLMODE: {
        ConfFieldKeys.TYPE: str,
        ConfFieldKeys.CHOICES: [
            "prefer",
            "require",
            "disable",
            "allow",
            "verify-ca",
            "verify-full",
        ],
        ConfFieldKeys.ENV: "DB_PGSSLMODE",
        ConfFieldKeys.TOML: f"{DatabaseKeys.DB}.{DatabaseKeys.SSLMODE}",
        ConfFieldKeys.DEFAULT: "prefer",
    },
}

INTERNATIONALIZATION_CONF_MAPPING: _MappingType = {
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

RUNCOMMANDS_CONF_MAPPING: _MappingType = {
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
