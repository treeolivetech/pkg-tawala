"""Package enumerations and constants."""

from enum import StrEnum
from pathlib import Path
from typing import Final

from christianwhocodes import Version


class Package:
    """Package metadata and paths as enum for easy access."""

    BASE_DIR: Final[Path] = Path(__file__).parent.resolve()
    CONTRIB_APPS_DIR: Final[Path] = BASE_DIR / "contrib"
    NAME: Final[str] = BASE_DIR.name
    DISPLAY_NAME: Final[str] = NAME.capitalize()
    SETTINGS_MODULE: Final[str] = f"{NAME}.management.settings"
    VERSION: Final[str] = Version.get(NAME)[0]


class Project:
    """Project-specific constants."""

    BASE_DIR: Final[Path] = Path.cwd()
    API_DIR: Final[Path] = BASE_DIR / "api"
    PUBLIC_DIR: Final[Path] = BASE_DIR / "public"
    HOME_APP_DIR: Final[Path] = BASE_DIR / "home"
    HOME_APP_NAME: Final[str] = HOME_APP_DIR.name


class InstalledApps(StrEnum):
    """Installed applications."""

    BROWSER_RELOAD = "django_browser_reload"
    WATCHFILES = "django_watchfiles"
    MINIFY_HTML = "django_minify_html"
    HTTP_COMPRESSION = "django_http_compression"
    SASS_PROCESSOR = "sass_processor"
    ADMIN = "django.contrib.admin"
    AUTH = "django.contrib.auth"
    CONTENTTYPES = "django.contrib.contenttypes"
    SESSIONS = "django.contrib.sessions"
    MESSAGES = "django.contrib.messages"
    STATICFILES = "django.contrib.staticfiles"


class Middlewares(StrEnum):
    """Middleware classes in recommended order."""

    SECURITY = "django.middleware.security.SecurityMiddleware"  # FIRST - security headers, HTTPS redirect
    SESSION = "django.contrib.sessions.middleware.SessionMiddleware"  # Early - needed by auth & messages
    COMMON = "django.middleware.common.CommonMiddleware"  # Early - URL normalization
    CSRF = "django.middleware.csrf.CsrfViewMiddleware"  # After session - needs session data
    AUTH = "django.contrib.auth.middleware.AuthenticationMiddleware"  # After session - stores user in session
    MESSAGES = "django.contrib.messages.middleware.MessageMiddleware"  # After session & auth
    CLICKJACKING = "django.middleware.clickjacking.XFrameOptionsMiddleware"  # Security headers (X-Frame-Options)
    CSP = "django.middleware.csp.ContentSecurityPolicyMiddleware"  # Security headers (Content-Security-Policy)
    HTTP_COMPRESSION = "django_http_compression.middleware.HttpCompressionMiddleware"  # Before any that modify html - encodes responses (Zstandard, Brotli, Gzip)
    MINIFY_HTML = "django_minify_html.middleware.MinifyHtmlMiddleware"  # After http_compression, before HTML modifiers
    BROWSER_RELOAD = (
        "django_browser_reload.middleware.BrowserReloadMiddleware"  # LAST - dev only, injects reload script into HTML
    )


class ContextProcessors(StrEnum):
    """Template context processors."""

    DEBUG = "django.template.context_processors.debug"  # Debug info (only in DEBUG mode)
    REQUEST = "django.template.context_processors.request"  # Adds request object to context
    AUTH = "django.contrib.auth.context_processors.auth"  # Adds user and perms to context
    MESSAGES = "django.contrib.messages.context_processors.messages"  # Adds messages to context
    CSP = "django.template.context_processors.csp"  # Content Security Policy


class StaticFileFinders(StrEnum):
    """Static file finders."""

    FILESYSTEM = "django.contrib.staticfiles.finders.FileSystemFinder"
    APPDIRECTORIES = "django.contrib.staticfiles.finders.AppDirectoriesFinder"
    SASS_PROCESSOR = "sass_processor.finders.CssFinder"


class AppDefMappings:
    """App definition Mappings."""

    APP_CONTEXT_PROCESSOR: Final[dict[InstalledApps, list[ContextProcessors]]] = {
        InstalledApps.AUTH: [ContextProcessors.AUTH],
        InstalledApps.MESSAGES: [ContextProcessors.MESSAGES],
    }
    APP_MIDDLEWARE: Final[dict[InstalledApps, list[Middlewares]]] = {
        InstalledApps.SESSIONS: [Middlewares.SESSION],
        InstalledApps.AUTH: [Middlewares.AUTH],
        InstalledApps.MESSAGES: [Middlewares.MESSAGES],
        InstalledApps.HTTP_COMPRESSION: [Middlewares.HTTP_COMPRESSION],
        InstalledApps.MINIFY_HTML: [Middlewares.MINIFY_HTML],
        InstalledApps.BROWSER_RELOAD: [Middlewares.BROWSER_RELOAD],
    }
    APP_STATICFILES_FINDERS: Final[dict[InstalledApps, list[str]]] = {
        InstalledApps.STATICFILES: [StaticFileFinders.FILESYSTEM, StaticFileFinders.APPDIRECTORIES],
        InstalledApps.SASS_PROCESSOR: [StaticFileFinders.SASS_PROCESSOR],
    }


class FileGenerateChoices(StrEnum):
    """Available file generation options."""

    README = "readme"
    API_SERVER_PY = "api/server.py"
    VERCEL_JSON = "vercel_json"
    PG_SERVICE = "pg_service"
    PGPASS = "pgpass"


class DatabaseChoices(StrEnum):
    """Available database backends."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class PostgresFlags(StrEnum):
    """Flag to indicate whether to use env / pyproject.toml variables for PostgreSQL configuration."""

    USE_VARS = "--pg-use-vars"


class StorageChoices(StrEnum):
    """Available storage backends."""

    FILESYSTEM = "filesystem"
    VERCELBLOB = "vercelblob"


class PresetChoices(StrEnum):
    """Available project presets."""

    DEFAULT = "default"
    VERCEL = "vercel"


class StorageTomlKeys(StrEnum):
    """Keys for storage configuration in pyproject.toml."""

    BACKEND = "backend"
    BLOB_TOKEN = "blob-token"


class DatabaseTomlKeys(StrEnum):
    """Keys for database configuration in pyproject.toml."""

    BACKEND = "backend"
    USE_VARS = "use-vars"
