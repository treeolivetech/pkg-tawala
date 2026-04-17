"""Settings enums."""

from enum import Enum, StrEnum
from typing import cast

# ============================================================================
# Module Exports
# ============================================================================
__all__ = [
    "SecurityKeys",
    "SecurityHelpTexts",
    "SecurityDebugOptions",
    "SecurityDefaults",
    "SecuritySecureSSLRedirectOptions",
    "SecuritySessionCookieSecureOptions",
    "SecurityCSRFCookieSecureOptions",
    "PresetKeys",
    "PresetHelpTexts",
    "PresetOptions",
    "PresetDefaults",
    "DatabaseKeys",
    "DatabaseHelpTexts",
    "DatabaseOptions",
    "DatabaseDefaults",
    "DatabaseUseVarsOptions",
    "DatabasePoolOptions",
    "DatabaseSSlModeOptions",
    "LayoutKeys",
    "LayoutHelpTexts",
    "LayoutOptions",
    "LayoutDefaults",
    "LayoutAlwaysShowAdminOptions",
    "InternationalizationKeys",
    "InternationalizationHelpTexts",
    "InternationalizationDefaults",
    "RuncommandKeys",
    "RuncommandHelpTexts",
    "RuncommandDefaults",
]


# ============================================================================
# Security & Deployment
# ============================================================================
class SecurityKeys(StrEnum):
    """Keys for security configuration in pyproject.toml."""

    ALLOWED_HOSTS = "allowed_hosts"
    SECRET_KEY = "secret_key"
    DEBUG_OPTION = "debug"
    SECURE_SSL_REDIRECT_OPTION = "secure_ssl_redirect"
    SESSION_COOKIE_SECURE_OPTION = "session_cookie_secure"
    CSRF_COOKIE_SECURE_OPTION = "csrf_cookie_secure"
    SECURE_HSTS_SECONDS = "secure_hsts_seconds"


# ---------------------------------


# debug
class SecurityDebugOptions(Enum):
    """Options for debug mode."""

    ENABLED = True
    DISABLED = False


# secure ssl redirect
class SecuritySecureSSLRedirectOptions(Enum):
    """Options for secure SSL redirect."""

    ENABLED = True
    DISABLED = False


# session cookie secure
class SecuritySessionCookieSecureOptions(Enum):
    """Options for session cookie security."""

    ENABLED = True
    DISABLED = False


# csrf cookie secure
class SecurityCSRFCookieSecureOptions(Enum):
    """Options for CSRF cookie security."""

    ENABLED = True
    DISABLED = False


# ---------------------------------


class SecurityDefaults(Enum):
    """Default values for security settings."""

    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    SECRET_KEY = "django-insecure-change-me-in-production-via-env-variable"
    DEBUG_OPTION = SecurityDebugOptions.ENABLED.value
    SECURE_SSL_REDIRECT_OPTION = SecuritySecureSSLRedirectOptions.DISABLED.value
    SESSION_COOKIE_SECURE_OPTION = SecuritySessionCookieSecureOptions.DISABLED.value
    CSRF_COOKIE_SECURE_OPTION = SecurityCSRFCookieSecureOptions.DISABLED.value
    SECURE_HSTS_SECONDS = 0


class SecurityHelpTexts(StrEnum):
    """Help texts for security configuration."""

    ALLOWED_HOSTS = "List of hostnames the app is allowed to serve."
    SECRET_KEY = (
        "Secret key used for cryptographic signing. Always set this in production."
    )
    DEBUG_OPTION = "Enable debug mode. Keep disabled in production environments."
    SECURE_SSL_REDIRECT_OPTION = "Redirect all HTTP requests to HTTPS when enabled."
    SESSION_COOKIE_SECURE_OPTION = (
        "Mark session cookies as secure so they are sent only over HTTPS."
    )
    CSRF_COOKIE_SECURE_OPTION = (
        "Mark CSRF cookies as secure so they are sent only over HTTPS."
    )
    SECURE_HSTS_SECONDS = "HTTP Strict Transport Security max-age value in seconds."


# ============================================================================
# Presets & Storages
# ============================================================================
class PresetKeys(StrEnum):
    """Keys for preset configuration in pyproject.toml."""

    PRESET = "preset"
    OPTION = "option"
    BLOB_TOKEN = "token"


# ---------------------------------


# option
class PresetOptions(StrEnum):
    """Available deployment preset backends."""

    DEFAULT = "default"
    VERCEL = "vercel"


# ---------------------------------


class PresetDefaults(Enum):
    """Preset Default values."""

    OPTION = PresetOptions.DEFAULT.value
    BLOB_TOKEN = "get-from-vercel-blob-storage-and-keep-private-via-env-var"


class PresetHelpTexts(StrEnum):
    """Help texts for preset configuration."""

    OPTION = "`default` or `vercel` preset that controls opinionated defaults for the project."
    BLOB_TOKEN = (
        "Token used for blob storage read/write access when blob support is enabled."
    )


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


# ---------------------------------
# option
class DatabaseOptions(StrEnum):
    """Available database backends."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


# use vars
class DatabaseUseVarsOptions(Enum):
    """Options for sourcing PostgreSQL settings from environment variables."""

    ENABLED = True
    DISABLED = False


# pool
class DatabasePoolOptions(Enum):
    """Options for enabling PostgreSQL connection pooling."""

    ENABLED = True
    DISABLED = False


# sslmode
class DatabaseSSlModeOptions(StrEnum):
    """Available database SSL modes."""

    DISABLED = "disabled"
    ALLOW = "allow"
    PREFER = "prefer"
    REQUIRE = "require"
    VERIFY_CA = "verify-ca"
    VERIFY_FULL = "verify-full"


# ---------------------------------


class DatabaseDefaults(Enum):
    """Default values for database settings."""

    OPTION = DatabaseOptions.SQLITE.value
    USE_VARS_OPTION = DatabaseUseVarsOptions.DISABLED.value
    SERVICE = ""
    USER = ""
    PASSWORD = ""
    NAME = ""
    HOST = ""
    PORT = 5432
    POOL_OPTION = DatabasePoolOptions.DISABLED.value
    SSLMODE_OPTION = DatabaseSSlModeOptions.PREFER.value


class DatabaseHelpTexts(StrEnum):
    """Help texts for database configuration."""

    OPTION = (
        "SQLite or PostgreSQL database backend to use. "
        "Automatically set to PostgreSQL if the preset option is set to Vercel. "
        "Defaults to SQLite for all other presets and when no preset is set."
    )
    USE_VARS_OPTION = (
        "Enable reading PostgreSQL connection values from individual DB_PG* variables. "
        "Automatically set to True if the preset option is set to Vercel. "
        "Defaults to False for all other presets and when no preset is set "
        "since it's more secure to use a pg_service and pg_pass configuration files."
    )
    SERVICE = "PostgreSQL service name from pg_service.conf, if `use-vars` option is disabled."
    USER = "PostgreSQL username for database authentication."
    PASSWORD = "PostgreSQL password for database authentication."
    NAME = "PostgreSQL database name to connect to."
    HOST = "PostgreSQL host or socket location."
    PORT = "PostgreSQL server port."
    POOL_OPTION = "Enable PostgreSQL connection pooling when supported."
    SSLMODE_OPTION = "PostgreSQL SSL mode for transport security."


# ============================================================================
# Layout
# ============================================================================
class LayoutKeys(StrEnum):
    """Keys for layout configuration in pyproject.toml."""

    LAYOUT = "layout"
    OPTION = "option"
    ALWAYS_SHOW_ADMIN_OPTION = "always_show_admin"


# ---------------------------------


class LayoutOptions(StrEnum):
    """Available layout options."""

    BASE = "base"
    WIP = "wip"


class LayoutAlwaysShowAdminOptions(Enum):
    """Options for always showing admin link in layout."""

    ENABLED = True
    DISABLED = False


# ---------------------------------


class LayoutDefaults(Enum):
    """Default values for layout configuration."""

    OPTION = LayoutOptions.BASE.value
    ALWAYS_SHOW_ADMIN_OPTION = LayoutAlwaysShowAdminOptions.DISABLED.value


class LayoutHelpTexts(StrEnum):
    """Help texts for layout configuration."""

    OPTION = "Primary layout template option used by the app."
    ALWAYS_SHOW_ADMIN_OPTION = (
        "Force admin links to display regardless of debug context."
    )


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


class InternationalizationDefaults(Enum):
    """Default values for internationalization configuration."""

    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "Africa/Nairobi"
    USE_I18N = True
    USE_TZ = True


class InternationalizationHelpTexts(StrEnum):
    """Help texts for internationalization configuration."""

    LANGUAGE_CODE = "Default language code used for internationalization."
    TIME_ZONE = "Default time zone used for date/time handling."
    USE_I18N = "Enable translation and locale machinery."
    USE_TZ = "Store and handle datetimes as timezone-aware values."


# ============================================================================
# Runcommands
# ============================================================================
class RuncommandKeys(StrEnum):
    """Keys for runcommands configuration in pyproject.toml."""

    RUNCOMMANDS = "runcommands"
    INSTALL = "install"
    BUILD = "build"


class RuncommandDefaults(Enum):
    """Default values for runcommands configuration."""

    INSTALL = cast(list[str], [])
    BUILD = [
        "makemigrations",
        "migrate",
        "compilescss",
        "collectstatic --noinput --ignore=*.scss",
    ]


class RuncommandHelpTexts(StrEnum):
    """Help texts for runcommands configuration."""

    INSTALL = "Management commands to run during project install/bootstrap."
    BUILD = "Management commands to run during build/deploy preparation."
