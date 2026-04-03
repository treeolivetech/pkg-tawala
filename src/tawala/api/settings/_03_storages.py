"""Files and Storage Configuration."""

from pathlib import Path
from typing import TypedDict

from ... import DefaultApps, Project, StorageChoices, StorageTomlKeys
from .. import ConfField, SettingsConf

__all__ = [
    "STORAGE_BACKEND",
    "BLOB_READ_WRITE_TOKEN",
    "STORAGES",
    "STATIC_ROOT",
    "STATIC_URL",
    "MEDIA_ROOT",
    "MEDIA_URL",
]


class _StorageConf(SettingsConf):
    """Files and Storage Configuration."""

    verbose_name = "03. Files and Storage Configuration"
    backend = ConfField(
        type=str,
        choices=[StorageChoices.FILESYSTEM, StorageChoices.VERCELBLOB],
        env="STORAGE_BACKEND",
        toml=f"storage.{StorageTomlKeys.BACKEND}",
        default=StorageChoices.FILESYSTEM,
    )
    token = ConfField(
        type=str,
        env="BLOB_READ_WRITE_TOKEN",
        toml=f"storage.{StorageTomlKeys.BLOB_TOKEN}",
        default="",
    )


_STORAGE = _StorageConf()
STORAGE_BACKEND: str = _STORAGE.backend
BLOB_READ_WRITE_TOKEN: str = _STORAGE.token


class _StorageBackendDict(TypedDict):
    """Individual storage backend entry."""

    BACKEND: str


class _StoragesDict(TypedDict):
    """STORAGES setting dict."""

    staticfiles: _StorageBackendDict
    default: _StorageBackendDict


def _get_storages_config() -> _StoragesDict:
    """Build the STORAGES setting based on configured backend."""
    storage_backend: str

    match STORAGE_BACKEND:
        case StorageChoices.FILESYSTEM:
            storage_backend = "django.core.files.storage.FileSystemStorage"
        case StorageChoices.VERCELBLOB:
            storage_backend = f"{DefaultApps.API}.backends.VercelBlobStorageBackend"
        case _:
            raise ValueError(f"Unsupported storage backend: {STORAGE_BACKEND}")

    return {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
        "default": {"BACKEND": storage_backend},
    }


STORAGES: _StoragesDict = _get_storages_config()
STATIC_ROOT: Path = Project.PUBLIC_DIR / "static"
STATIC_URL: str = "static/"
MEDIA_ROOT: Path = Project.PUBLIC_DIR / "media"
MEDIA_URL: str = "media/"
