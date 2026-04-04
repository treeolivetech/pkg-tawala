"""Enumerations and constants."""

from enum import StrEnum

__all__ = ["DatabaseTomlKeys", "DatabaseBackends"]


class DatabaseTomlKeys(StrEnum):
    """Keys for database configuration in pyproject.toml."""

    MAIN = "db"
    BACKEND = "backend"
    USE_VARS = "use-vars"
    SERVICE = "service"
    USER = "user"
    PASSWORD = "password"
    NAME = "name"
    HOST = "host"
    PORT = "port"
    POOL = "pool"
    SSLMODE = "sslmode"


class DatabaseBackends(StrEnum):
    """Available database backends."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
