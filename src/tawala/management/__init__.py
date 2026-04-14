"""Management module constants."""

from enum import StrEnum


# ============================================================================
# ConfField
# ============================================================================
class ConfFieldKeys(StrEnum):
    """Namings for various components."""

    TYPE = "type"
    CHOICES = "choices"
    ENV = "env"
    TOML = "toml"
    DEFAULT = "default"


# ============================================================================
# Presets & Storages
# ============================================================================
class PresetOptions(StrEnum):
    """Available database backends."""

    DEFAULT = "default"
    VERCEL = "vercel"


class PresetKeys(StrEnum):
    """Keys for preset configuration in pyproject.toml."""

    PRESET = "preset"
    BACKEND = "backend"
    BLOB_TOKEN = "blob-token"


class PresetFlags(StrEnum):
    """Flags used when setting up preset during initialization."""

    PRESET = f"--{PresetKeys.PRESET}"

    @property
    def dest(self):  # noqa: D102
        return self.value.lstrip("-").replace("-", "_")


# ============================================================================
# Databases
# ============================================================================
class DatabaseOptions(StrEnum):
    """Available database backends."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class DatabaseKeys(StrEnum):
    """Keys for database configuration in pyproject.toml."""

    DB = "db"
    BACKEND = "backend"
    USE_VARS = "pg-use-vars"
    SERVICE = "pg-service"
    USER = "pg-user"
    PASSWORD = "pg-password"
    NAME = "pg-database"
    HOST = "pg-host"
    PORT = "pg-port"
    POOL = "pg-pool"
    SSLMODE = "pg-sslmode"


class DatabaseFlags(StrEnum):
    """Flags used when setting up database during initialization."""

    DB = f"--{DatabaseKeys.DB}"
    PG_USE_VARS = f"--{DatabaseKeys.USE_VARS}"

    @property
    def dest(self):  # noqa: D102
        return self.value.lstrip("-").replace("-", "_")


# ============================================================================
# Internationalization
# ============================================================================
class InternationalizationKeys(StrEnum):
    """Keys for internationalization configuration in pyproject.toml."""

    INTERNATIONALIZATION = "internationalization"
    LANGUAGE_CODE = "language-code"
    TIME_ZONE = "time-zone"
    USE_I18N = "use-i18n"
    USE_TZ = "use-tz"


# ============================================================================
# Runcommands
# ============================================================================
class RuncommandKeys(StrEnum):
    """Keys for runcommands configuration in pyproject.toml."""

    RUNCOMMANDS = "runcommands"
    INSTALL = "install"
    BUILD = "build"


# ============================================================================
# Security
# ============================================================================
class SecurityKeys(StrEnum):
    """Keys for security configuration in pyproject.toml."""

    SECRET_KEY = "secret-key"
    DEBUG = "debug"
    ALLOWED_HOSTS = "allowed-hosts"
    SECURE_SSL_REDIRECT = "secure-ssl-redirect"
    SESSION_COOKIE_SECURE = "session-cookie-secure"
    CSRF_COOKIE_SECURE = "csrf-cookie-secure"
    SECURE_HSTS_SECONDS = "secure-hsts-seconds"
    WORK_IN_PROGRESS = "work-in-progress"
    ADMIN_ENABLED = "admin-enabled"
