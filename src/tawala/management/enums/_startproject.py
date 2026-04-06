from enum import StrEnum

__all__ = [
    "PresetOptions",
    "PresetFlags",
    "StorageTomlKeys",
    "StorageBackendOptions",
    "DatabaseTomlKeys",
    "DatabaseBackendOptions",
    "DatabaseFlags",
]


class PresetOptions(StrEnum):
    """Available database backends."""

    DEFAULT = "default"
    VERCEL = "vercel"


class PresetFlags(StrEnum):
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


class StorageBackendOptions(StrEnum):
    """Available storage backends."""

    FILESYSTEM = "filesystem"
    VERCEL = "vercel"


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


class DatabaseBackendOptions(StrEnum):
    """Available database backends."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class DatabaseFlags(StrEnum):
    """Flags used when setting up database during initialization."""

    DB = "--db"
    USE_VARS = "--pg-use-vars"
