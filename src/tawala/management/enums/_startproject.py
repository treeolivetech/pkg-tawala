from enum import StrEnum

__all__ = [
    "PresetChoices",
    "PresetInitFlags",
    "StorageTomlKeys",
    "StorageBackends",
    "DatabaseTomlKeys",
    "DatabaseBackends",
    "DatabaseInitFlags",
]


class PresetChoices(StrEnum):
    """Available database backends."""

    DEFAULT = "default"
    VERCEL = "vercel"


class PresetInitFlags(StrEnum):
    """Flags used when setting up preset during initialization."""

    PRESET = "--preset"


# ============================================================================
# Storages
# ============================================================================


class StorageTomlKeys(StrEnum):
    """Keys for storage configuration in pyproject.toml."""

    MAIN = "storage"
    BACKEND = "backend"
    BLOB_TOKEN = "blob-token"


class StorageBackends(StrEnum):
    """Available storage backends."""

    FILESYSTEM = "filesystem"
    VERCEL = "vercelblob"


# ============================================================================
# Databases
# ============================================================================


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


class DatabaseInitFlags(StrEnum):
    """Flags used when setting up database during initialization."""

    DB = "--db"
    USE_VARS = "--pg-use-vars"
