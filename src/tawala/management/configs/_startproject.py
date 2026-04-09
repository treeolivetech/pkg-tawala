from ..enums import DatabaseBackendOptions, DatabaseTomlKeys, StorageBackendOptions, StorageTomlKeys
from ._utils import Conf, ConfField

__all__ = ["STORAGES_CONF", "DATABASES_CONF"]

# ============================================================================
# Storages
# ============================================================================


class _StoragesConf(Conf):
    """Files and Storage Configuration."""

    verbose_name = "Files and Storage Configuration"
    backend = ConfField(
        type=str,
        choices=[StorageBackendOptions.DEFAULT, StorageBackendOptions.VERCEL],
        env="STORAGE_BACKEND",
        toml=f"{StorageTomlKeys.MAIN}.{StorageTomlKeys.BACKEND}",
        default=StorageBackendOptions.DEFAULT,
    )
    token = ConfField(
        type=str,
        env="BLOB_READ_WRITE_TOKEN",
        toml=f"{StorageTomlKeys.MAIN}.{StorageTomlKeys.BLOB_TOKEN}",
        default="",
    )


STORAGES_CONF = _StoragesConf()


# ============================================================================
# Databases
# ============================================================================


class _DatabasesConf(Conf):
    """Database Configuration."""

    verbose_name = "Database Configuration"

    backend = ConfField(
        type=str,
        choices=[c for c in DatabaseBackendOptions],
        env="DB_BACKEND",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.BACKEND}",
        default=DatabaseBackendOptions.SQLITE,
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
        env="DB_PGSERVICE",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.SERVICE}",
        default="",
    )
    user = ConfField(
        type=str,
        env="DB_PGUSER",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.USER}",
        default="",
    )
    password = ConfField(
        type=str,
        env="DB_PGPASSWORD",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.PASSWORD}",
        default="",
    )
    name = ConfField(
        type=str,
        env="DB_PGDATABASE",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.NAME}",
        default="",
    )
    host = ConfField(
        type=str,
        env="DB_PGHOST",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.HOST}",
        default="localhost",
    )
    port = ConfField(
        type=int,
        env="DB_PGPORT",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.PORT}",
        default=5432,
    )
    pool = ConfField(
        type=bool,
        env="DB_PGPOOL",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.POOL}",
        default=False,
    )
    sslmode = ConfField(
        type=str,
        choices=["prefer", "require", "disable", "allow", "verify-ca", "verify-full"],
        env="DB_PGSSLMODE",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.SSLMODE}",
        default="prefer",
    )


DATABASES_CONF = _DatabasesConf()
