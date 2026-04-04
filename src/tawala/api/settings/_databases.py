"""Databases Configuration.

https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes
https://www.postgresql.org/docs/current/libpq-pgservice.html
https://www.postgresql.org/docs/current/libpq-pgpass.html
"""

from pathlib import Path
from typing import NotRequired, TypedDict

from ... import PROJECT
from ..enums import DatabaseBackends, DatabaseTomlKeys
from .conf import Conf, ConfField

__all__ = ["DATABASES"]

# ============================================================================
# Typed dictionaries
# ============================================================================


class _DatabaseOptionsDict(TypedDict, total=False):
    """Database OPTIONS dict."""

    service: str
    pool: bool
    sslmode: str


class DatabaseDict(TypedDict):
    """Single database configuration entry."""

    ENGINE: str
    NAME: str | Path
    USER: NotRequired[str | None]
    PASSWORD: NotRequired[str | None]
    HOST: NotRequired[str | None]
    PORT: NotRequired[str | None]
    OPTIONS: NotRequired[_DatabaseOptionsDict]


class DatabasesDict(TypedDict):
    """DATABASES setting dict."""

    default: DatabaseDict


# ============================================================================
# Configuration fields
# ============================================================================


class _DatabaseConf(Conf):
    """Database Configuration."""

    verbose_name = "Database Configuration"

    backend = ConfField(
        type=str,
        choices=[c for c in DatabaseBackends],
        env="DB_BACKEND",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.BACKEND}",
        default=DatabaseBackends.SQLITE,
    )
    # postgresql specific
    use_vars = ConfField(
        type=bool,
        env="DB_USE_VARS",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.USE_VARS}",
        default=False,
    )
    service = ConfField(
        type=str,
        env="DB_SERVICE",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.SERVICE}",
        default="",
    )
    user = ConfField(
        type=str,
        env="DB_USER",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.USER}",
        default="",
    )
    password = ConfField(
        type=str,
        env="DB_PASSWORD",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.PASSWORD}",
        default="",
    )
    name = ConfField(
        type=str,
        env="DB_NAME",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.NAME}",
        default="",
    )
    host = ConfField(
        type=str,
        env="DB_HOST",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.HOST}",
        default="localhost",
    )
    port = ConfField(
        type=int,
        env="DB_PORT",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.PORT}",
        default=5432,
    )
    pool = ConfField(
        type=bool,
        env="DB_POOL",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.POOL}",
        default=False,
    )
    sslmode = ConfField(
        type=str,
        choices=["prefer", "require", "disable", "allow", "verify-ca", "verify-full"],
        env="DB_SSLMODE",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.SSLMODE}",
        default="prefer",
    )


_DATABASE = _DatabaseConf()


# ============================================================================
# Builders
# ============================================================================


def _get_databases_config() -> DatabasesDict:
    """Build the DATABASES setting based on configured backend."""
    backend: str = _DATABASE.backend.lower()
    match backend:
        case DatabaseBackends.SQLITE:
            return {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": PROJECT.base_dir / f"db.sqlite3",
                }
            }
        case DatabaseBackends.POSTGRESQL:
            config: DatabaseDict
            if _DATABASE.use_vars:
                config = {
                    "ENGINE": f"django.db.backends.postgresql",
                    "NAME": _DATABASE.name,
                    "USER": _DATABASE.user,
                    "PASSWORD": _DATABASE.password,
                    "HOST": _DATABASE.host,
                    "PORT": str(_DATABASE.port),
                    "OPTIONS": {"pool": _DATABASE.pool, "sslmode": _DATABASE.sslmode},
                }
            else:
                config = {
                    "ENGINE": f"django.db.backends.postgresql",
                    "NAME": _DATABASE.name,
                    "OPTIONS": {
                        "pool": _DATABASE.pool,
                        "sslmode": _DATABASE.sslmode,
                        "service": _DATABASE.service,
                    },
                }
            return {"default": config}
        case _:
            pass

    raise ValueError(f"Unsupported DB backend: {backend}")


# ============================================================================
# Public variables
# ============================================================================

DATABASES = _get_databases_config()
