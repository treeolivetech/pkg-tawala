from pathlib import Path
from typing import NotRequired, TypedDict

__all__ = ["StoragesDict", "DatabaseDict", "DatabasesDict"]

# ============================================================================
# Storages
# ============================================================================


class _StorageBackendDict(TypedDict):
    """Individual storage backend entry."""

    BACKEND: str


class StoragesDict(TypedDict):
    """STORAGES setting dict."""

    staticfiles: _StorageBackendDict
    default: _StorageBackendDict


# ============================================================================
# Databases
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
