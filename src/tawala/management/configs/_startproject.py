from ..enums import DatabaseBackends, DatabaseTomlKeys, StorageBackends, StorageTomlKeys
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
        choices=[StorageBackends.FILESYSTEM, StorageBackends.VERCEL],
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


STORAGES_CONF = _StoragesConf()


# ============================================================================
# Databases
# ============================================================================


class _DatabasesConf(Conf):
    """Database Configuration."""

    verbose_name = "Database Configuration"

    backend = ConfField(
        type=str,
        choices=[c for c in DatabaseBackends],
        env="DB_BACKEND",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.BACKEND}",
        default=DatabaseBackends.SQLITE,
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
        env="DB_SERVICE",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.SERVICE}",
        default="",
    )
    user = ConfField(
        type=str,
        env="DB_USER",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.USER}",
        default="",
    )
    password = ConfField(
        type=str,
        env="DB_PASSWORD",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.PASSWORD}",
        default="",
    )
    name = ConfField(
        type=str,
        env="DB_NAME",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.NAME}",
        default="",
    )
    host = ConfField(
        type=str,
        env="DB_HOST",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.HOST}",
        default="localhost",
    )
    port = ConfField(
        type=int,
        env="DB_PORT",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.PORT}",
        default=5432,
    )
    pool = ConfField(
        type=bool,
        env="DB_POOL",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.POOL}",
        default=False,
    )
    sslmode = ConfField(
        type=str,
        choices=["prefer", "require", "disable", "allow", "verify-ca", "verify-full"],
        env="DB_SSLMODE",
        toml=f"{DatabaseTomlKeys.MAIN}.{DatabaseTomlKeys.SSLMODE}",
        default="prefer",
    )


DATABASES_CONF = _DatabasesConf()
