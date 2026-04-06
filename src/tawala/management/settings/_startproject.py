from ... import PROJECT, Package
from ..configs import DATABASES_CONF, STORAGES_CONF
from ..enums import DatabaseBackendOptions, StorageBackendOptions
from ..typings import DatabaseDict, DatabasesDict, StoragesDict

__all__ = [
    "STORAGES",
    "STATIC_ROOT",
    "MEDIA_ROOT",
    "STATIC_URL",
    "MEDIA_URL",
    "DATABASES",
]

# ============================================================================
# Storages
# ============================================================================


def get_storages_config(storage_backend_choice: str) -> StoragesDict:
    """Build the STORAGES setting based on configured backend."""
    storage_backend: str

    match storage_backend_choice:
        case StorageBackendOptions.FILESYSTEM:
            storage_backend = "django.core.files.storage.FileSystemStorage"
        case StorageBackendOptions.VERCEL:
            storage_backend = f"{Package.MANAGEMENT}.backends.VercelBlobStorageBackend"
        case _:
            raise ValueError(f"Unsupported storage backend: {storage_backend_choice}")

    return {
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
        "default": {"BACKEND": storage_backend},
    }


STORAGES = get_storages_config(STORAGES_CONF.backend)


# ============================================================================
# Static & Media
# ============================================================================

_PUBLIC_DIR = PROJECT.base_dir / "public"

STATIC_ROOT = _PUBLIC_DIR / "static"

MEDIA_ROOT = _PUBLIC_DIR / "media"

STATIC_URL = "static/"

MEDIA_URL = "media/"


# ============================================================================
# Databases
# https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes
# https://www.postgresql.org/docs/current/libpq-pgservice.html
# https://www.postgresql.org/docs/current/libpq-pgpass.html
# ============================================================================


def _get_databases_config() -> DatabasesDict:
    """Build the DATABASES setting based on configured backend."""
    backend: str = DATABASES_CONF.backend.lower()
    match backend:
        case DatabaseBackendOptions.SQLITE:
            return {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": PROJECT.base_dir / f"db.sqlite3",
                }
            }
        case DatabaseBackendOptions.POSTGRESQL:
            config: DatabaseDict
            if DATABASES_CONF.use_vars:
                config = {
                    "ENGINE": f"django.db.backends.postgresql",
                    "NAME": DATABASES_CONF.name,
                    "USER": DATABASES_CONF.user,
                    "PASSWORD": DATABASES_CONF.password,
                    "HOST": DATABASES_CONF.host,
                    "PORT": str(DATABASES_CONF.port),
                    "OPTIONS": {"pool": DATABASES_CONF.pool, "sslmode": DATABASES_CONF.sslmode},
                }
            else:
                config = {
                    "ENGINE": f"django.db.backends.postgresql",
                    "NAME": DATABASES_CONF.name,
                    "OPTIONS": {
                        "pool": DATABASES_CONF.pool,
                        "sslmode": DATABASES_CONF.sslmode,
                        "service": DATABASES_CONF.service,
                    },
                }
            return {"default": config}
        case _:
            pass

    raise ValueError(f"Unsupported DB backend: {backend}")


DATABASES = _get_databases_config()
