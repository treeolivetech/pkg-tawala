from enum import StrEnum

__all__ = ["StorageTomlKeys", "StorageBackends"]


class StorageTomlKeys(StrEnum):
    """Keys for storage configuration in pyproject.toml."""

    MAIN = "storage"
    BACKEND = "backend"
    BLOB_TOKEN = "blob-token"


class StorageBackends(StrEnum):
    """Available storage backends."""

    FILESYSTEM = "filesystem"
    VERCELBLOB = "vercelblob"
