from typing import TypedDict

from ... import Package
from ..enums import StorageBackends, StorageTomlKeys
from ._startproject import PROJECT
from ._startproject import Conf, ConfField

__all__ = [
    "STORAGE_BACKEND",
    "BLOB_READ_WRITE_TOKEN",
    "STORAGES",
    "STATIC_ROOT",
    "STATIC_URL",
    "MEDIA_ROOT",
    "MEDIA_URL",
]


# ============================================================================
# Typed dictionaries
# ============================================================================


class _StorageBackendDict(TypedDict):
    """Individual storage backend entry."""

    BACKEND: str


class _StoragesDict(TypedDict):
    """STORAGES setting dict."""

    staticfiles: _StorageBackendDict
    default: _StorageBackendDict


# ============================================================================
# Configuration fields
# ============================================================================


class _StorageConf(Conf):
    """Files and Storage Configuration."""

    verbose_name = "Files and Storage Configuration"
    backend = ConfField(
        type=str,
        choices=[StorageBackends.FILESYSTEM, StorageBackends.VERCELBLOB],
        env="STORAGE_BACKEND",
        toml=f"{StorageTomlKeys.MAIN}.{StorageTomlKeys.BACKEND}",
        default=StorageBackends.FILESYSTEM,
    )
    token = ConfField(
        type=str,
        env="BLOB_READ_WRITE_TOKEN",
        toml=f"{StorageTomlKeys.MAIN}.{StorageTomlKeys.BLOB_TOKEN}",
        default="",
    )


_STORAGE = _StorageConf()

# ============================================================================
# Builders
# ============================================================================


def _get_storages_config(storage_backend_choice: str) -> _StoragesDict:
    """Build the STORAGES setting based on configured backend."""
    storage_backend: str

    match storage_backend_choice:
        case StorageBackends.FILESYSTEM:
            storage_backend = "django.core.files.storage.FileSystemStorage"
        case StorageBackends.VERCELBLOB:
            storage_backend = f"{Package.API}.backends.VercelBlobStorageBackend"
        case _:
            raise ValueError(f"Unsupported storage backend: {storage_backend_choice}")

    return {
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
        "default": {"BACKEND": storage_backend},
    }


_PUBLIC_DIR = PROJECT.base_dir / "public"


# ============================================================================
# Public variables
# ============================================================================

STORAGE_BACKEND: str = _STORAGE.backend

BLOB_READ_WRITE_TOKEN: str = _STORAGE.token

STORAGES = _get_storages_config(STORAGE_BACKEND)

STATIC_ROOT = _PUBLIC_DIR / "static"

STATIC_URL = "static/"

MEDIA_ROOT = _PUBLIC_DIR / "media"

MEDIA_URL = "media/"
