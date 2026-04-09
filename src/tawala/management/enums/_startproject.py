from enum import StrEnum

__all__ = [
    "ProjectPresetOptions",
    "ProjectPresetFlags",
    "StorageTomlKeys",
    "StorageBackendOptions",
    "DatabaseTomlKeys",
    "DatabaseBackendOptions",
    "DatabaseFlags",
]


# ============================================================================
# Project Presets
# ============================================================================


class ProjectPresetOptions(StrEnum):
    """Available database backends."""

    DEFAULT = "default"
    VERCEL = "vercel"


class ProjectPresetFlags(StrEnum):
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

    DEFAULT = ProjectPresetOptions.DEFAULT.value
    VERCEL = ProjectPresetOptions.VERCEL.value


# ============================================================================
# Databases
# ============================================================================


class DatabaseTomlKeys(StrEnum):
    """Keys for database configuration in pyproject.toml."""

    MAIN = "db"
    BACKEND = "backend"
    USE_VARS = "use-vars"
    SERVICE = "pgservice"
    USER = "pguser"
    PASSWORD = "pgpassword"
    NAME = "pgdatabase"
    HOST = "pghost"
    PORT = "pgport"
    POOL = "pgpool"
    SSLMODE = "pgsslmode"


class DatabaseBackendOptions(StrEnum):
    """Available database backends."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class DatabaseFlags(StrEnum):
    """Flags used when setting up database during initialization."""

    DB = "--db"
    USE_VARS = "--pg-use-vars"
