"""Settings enums."""

from enum import Enum, StrEnum

# ============================================================================
# Module Exports
# ============================================================================
__all__ = [
    "SecurityKeys",
    "SecurityDebugOptions",
    "SecurityAllowedHostsDefaults",
    "PresetKeys",
    "PresetOptions",
    "PresetBlobTokenDefaults",
    "DatabaseKeys",
    "DatabaseOptions",
    "DatabaseUseVarsOptions",
    "DatabasePoolOptions",
    "DatabaseSSlModeOptions",
    "LayoutKeys",
    "LayoutOptions",
    "LayoutAlwaysShowAdminOptions",
    "InternationalizationKeys",
    "RuncommandKeys",
]


# ============================================================================
# Security & Deployment
# ============================================================================
class SecurityKeys(StrEnum):
    """Keys for security configuration in pyproject.toml."""

    SECRET_KEY = "secret_key"
    DEBUG_OPTION = "debug"
    ALLOWED_HOSTS = "allowed_hosts"
    SECURE_SSL_REDIRECT = "secure_ssl_redirect"
    SESSION_COOKIE_SECURE = "session_cookie_secure"
    CSRF_COOKIE_SECURE = "csrf_cookie_secure"
    SECURE_HSTS_SECONDS = "secure_hsts_seconds"


class SecurityDebugOptions(Enum):
    """Options for debug mode."""

    DEFAULT_ENABLED = True
    DISABLED = False


class SecurityAllowedHostsDefaults(StrEnum):
    """Default values for allowed hosts."""

    LOCALHOST_DOMAIN = "localhost"
    LOCALHOST_IP = "127.0.0.1"


# ============================================================================
# Presets & Storages
# ============================================================================
class PresetKeys(StrEnum):
    """Keys for preset configuration in pyproject.toml."""

    PRESET = "preset"
    OPTION = "option"
    BLOB_TOKEN = "token"


class PresetOptions(StrEnum):
    """Available deployment preset backends."""

    DEFAULT = "default"
    VERCEL = "vercel"


class PresetBlobTokenDefaults(StrEnum):
    """Default values for blob token."""

    GET_FROM_VERCEL = "get-from-vercel-blob-storage-and-keep-private-via-env-var"


# ============================================================================
# Databases
# ============================================================================
class DatabaseKeys(StrEnum):
    """Keys for database configuration in pyproject.toml."""

    DB = "db"
    OPTION = "option"
    USE_VARS_OPTION = "pg_use_vars"
    SERVICE = "pg_service"
    USER = "pg_user"
    PASSWORD = "pg_password"
    NAME = "pg_database"
    HOST = "pg_host"
    PORT = "pg_port"
    POOL_OPTION = "pg_pool"
    SSLMODE_OPTION = "pg_sslmode"


class DatabaseOptions(StrEnum):
    """Available database backends."""

    DEFAULT_SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class DatabaseUseVarsOptions(Enum):
    """Options for sourcing PostgreSQL settings from environment variables."""

    ENABLED = True
    DEFAULT_DISABLED = False


class DatabasePoolOptions(Enum):
    """Options for enabling PostgreSQL connection pooling."""

    ENABLED = True
    DEFAULT_DISABLED = False


class DatabaseSSlModeOptions(StrEnum):
    """Available database SSL modes."""

    DISABLED = "disabled"
    ALLOW = "allow"
    DEFAULT_PREFER = "prefer"
    REQUIRE = "require"
    VERIFY_CA = "verify-ca"
    VERIFY_FULL = "verify-full"


# ============================================================================
# Layout
# ============================================================================
class LayoutKeys(StrEnum):
    """Keys for layout configuration in pyproject.toml."""

    LAYOUT = "layout"
    OPTION = "option"
    ALWAYS_SHOW_ADMIN_OPTION = "always_show_admin"


class LayoutOptions(StrEnum):
    """Available layout options."""

    DEFAULT_BASE = "base"
    WIP = "wip"


class LayoutAlwaysShowAdminOptions(Enum):
    """Options for always showing admin link in layout."""

    ENABLED = True
    DEFAULT_DISABLED = False


# ============================================================================
# Internationalization
# ============================================================================
class InternationalizationKeys(StrEnum):
    """Keys for internationalization configuration in pyproject.toml."""

    INTERNATIONALIZATION = "internationalization"
    LANGUAGE_CODE = "language_code"
    TIME_ZONE = "time_zone"
    USE_I18N = "use_i18n"
    USE_TZ = "use_tz"


# ============================================================================
# Runcommands
# ============================================================================
class RuncommandKeys(StrEnum):
    """Keys for runcommands configuration in pyproject.toml."""

    RUNCOMMANDS = "runcommands"
    INSTALL = "install"
    BUILD = "build"
