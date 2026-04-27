"""Main settings."""

from pathlib import Path
from typing import NotRequired, TypeAlias, TypedDict

from django.utils.csp import CSP  # pyright: ignore[reportMissingTypeStubs]
from treeolive_api.conf import (
    API_APP,
    FETCH_DATABASES,
    FETCH_INTERNATIONALIZATION,
    FETCH_LAYOUT,
    FETCH_PRESET,
    FETCH_PROJECT,
    FETCH_RUNCOMMANDS,
    FETCH_SECURITY,
    DatabaseOptions,
    LayoutOptions,
    PresetOptions,
)
from treeolive_ui.conf import UI_APP

# ============================================================================
# Core & Installed applications
# ============================================================================


BASE_DIR = FETCH_PROJECT.base_dir

CORE_APP = FETCH_PROJECT.core_app
CORE_NAME = FETCH_PROJECT.core_name
CORE_DISPLAY_NAME = FETCH_PROJECT.core_display_name
CORE_VERSION = FETCH_PROJECT.core_version

_ASSETS_STR = "assets"
_WIDGETS_STR = "widgets"
_LAYOUTS_STR = "layouts"

ASSET_APPS = f"{UI_APP}.components.{_ASSETS_STR}"
WIDGET_APPS = f"{UI_APP}.components.{_WIDGETS_STR}"
LAYOUT_APPS = f"{UI_APP}.components.{_LAYOUTS_STR}"


MAIN_APP = "app"

INSTALLED_APPS = [
    "django_browser_reload",
    "django_minify_html",
    "django_http_compression",
    MAIN_APP,
]

match FETCH_LAYOUT.option:
    case LayoutOptions.WIP.value:
        INSTALLED_APPS.extend([f"{LAYOUT_APPS}.{LayoutOptions.WIP.value}"])
    case _:
        INSTALLED_APPS.extend([
            *([f"{WIDGET_APPS}.addresses", "phonenumber_field"]),
            f"{WIDGET_APPS}.footer",
            f"{WIDGET_APPS}.header",
            f"{WIDGET_APPS}.scroll_top",
            f"{WIDGET_APPS}.logout",
            f"{WIDGET_APPS}.preloader",
            f"{ASSET_APPS}.bootstrap",
            f"{ASSET_APPS}.aos",
        ])

INSTALLED_APPS.extend([
    CORE_APP,
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    *(["sass_processor", "django.contrib.staticfiles"]),
])


# ============================================================================
# Security & Deployment
# https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
# https://docs.djangoproject.com/en/stable/howto/csp/
# ============================================================================
SECRET_KEY = FETCH_SECURITY.secret_key
DEBUG = FETCH_SECURITY.debug_option
ALLOWED_HOSTS = FETCH_SECURITY.allowed_hosts
SECURE_SSL_REDIRECT = FETCH_SECURITY.secure_ssl_redirect
SESSION_COOKIE_SECURE = FETCH_SECURITY.session_cookie_secure
CSRF_COOKIE_SECURE = FETCH_SECURITY.csrf_cookie_secure
SECURE_HSTS_SECONDS = FETCH_SECURITY.secure_hsts_seconds

SECURE_CSP: dict[str, list[str]] = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE],
    "style-src": [
        CSP.SELF,
        CSP.NONCE,
        "https://fonts.googleapis.com",  # Google Fonts CSS
    ],
    "font-src": [
        CSP.SELF,
        "https://fonts.gstatic.com",  # Google Fonts font files
    ],
}


# ============================================================================
# Middleware
# ============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "django_http_compression.middleware.HttpCompressionMiddleware",  # Before any that modify html
    "django_minify_html.middleware.MinifyHtmlMiddleware",  # After http_compression, before HTML modifiers
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]


# ============================================================================
# ASGI, WSGI
# ============================================================================

WSGI_APPLICATION = f"{CORE_APP}.management.contrib.api.server"


# ============================================================================
# Root URLConf
# ============================================================================
ROOT_URLCONF = f"{CORE_APP}.urls"


# ============================================================================
# Templates
# ============================================================================
class _TemplateOptionsDict(TypedDict):
    """Template OPTIONS dict."""

    context_processors: list[str]
    builtins: NotRequired[list[str]]
    libraries: NotRequired[dict[str, str]]


class _TemplateDict(TypedDict):
    """Single TEMPLATES entry."""

    BACKEND: str
    DIRS: list[Path]
    APP_DIRS: bool
    OPTIONS: _TemplateOptionsDict


_TemplatesDict: TypeAlias = list[_TemplateDict]

TEMPLATES: _TemplatesDict = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.csp",
            ],
            "libraries": {
                _ASSETS_STR: f"{ASSET_APPS}.templatetags",
                _WIDGETS_STR: f"{WIDGET_APPS}.templatetags",
                _LAYOUTS_STR: f"{LAYOUT_APPS}.templatetags",
            },
        },
    }
]


# ============================================================================
# Staticfiles, Media & Sass
# ============================================================================
PUBLIC_DIR = BASE_DIR / "public"
STATIC_ROOT = PUBLIC_DIR / "static"
MEDIA_ROOT = PUBLIC_DIR / "media"

STATIC_URL = "static/"
MEDIA_URL = "media/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

SASS_PRECISION = 8


# ============================================================================
# Presets & Storages
# ============================================================================
class _StorageBackendDict(TypedDict):
    """Individual storage backend entry."""

    BACKEND: str


class _StoragesDict(TypedDict):
    """STORAGES setting dict."""

    staticfiles: _StorageBackendDict
    default: _StorageBackendDict


def get_storages_config(preset_option: str) -> _StoragesDict:
    """Build the STORAGES setting based on configured backend."""
    storage_backend: str

    match preset_option:
        case PresetOptions.DEFAULT.value:
            storage_backend = "django.core.files.storage.FileSystemStorage"
        case PresetOptions.VERCEL.value:
            storage_backend = f"{API_APP}.contrib.vercel.storage.VercelBlobStorage"
        case _:
            raise ValueError(f"Unsupported storage backend: {preset_option}")

    return {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
        "default": {"BACKEND": storage_backend},
    }


STORAGES = get_storages_config(FETCH_PRESET.option)
BLOB_READ_WRITE_TOKEN = FETCH_PRESET.blob_read_write_token


# ============================================================================
# Databases
# https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes
# https://www.postgresql.org/docs/current/libpq-pgservice.html
# https://www.postgresql.org/docs/current/libpq-pgpass.html
# ============================================================================
class _DatabaseMoreOptionsDict(TypedDict, total=False):
    """Database OPTIONS dict."""

    service: str
    pool: bool
    sslmode: str


class _DatabaseDict(TypedDict):
    """Single database configuration entry."""

    ENGINE: str
    NAME: str | Path
    USER: NotRequired[str | None]
    PASSWORD: NotRequired[str | None]
    HOST: NotRequired[str | None]
    PORT: NotRequired[str | None]
    OPTIONS: NotRequired[_DatabaseMoreOptionsDict]


class _DatabasesDict(TypedDict):
    """DATABASES setting dict."""

    default: _DatabaseDict


def _get_databases_config() -> _DatabasesDict:
    """Build the DATABASES setting based on configured backend."""
    backend: str = FETCH_DATABASES.option.lower()
    match backend:
        case DatabaseOptions.SQLITE.value:
            return {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": BASE_DIR / "db.sqlite3",
                }
            }
        case DatabaseOptions.POSTGRESQL.value:
            config: _DatabaseDict
            if FETCH_DATABASES.pg_use_vars:
                config = {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": FETCH_DATABASES.pg_database,
                    "USER": FETCH_DATABASES.pg_user,
                    "PASSWORD": FETCH_DATABASES.pg_password,
                    "HOST": FETCH_DATABASES.pg_host,
                    "PORT": str(FETCH_DATABASES.pg_port),
                    "OPTIONS": {
                        "pool": FETCH_DATABASES.pg_pool,
                        "sslmode": FETCH_DATABASES.pg_sslmode,
                    },
                }
            else:
                config = {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": FETCH_DATABASES.pg_database,
                    "OPTIONS": {
                        "pool": FETCH_DATABASES.pg_pool,
                        "sslmode": FETCH_DATABASES.pg_sslmode,
                        "service": FETCH_DATABASES.pg_service,
                    },
                }
            return {"default": config}
        case _:
            pass

    raise ValueError(f"Unsupported DB backend: {backend}")


DATABASES = _get_databases_config()


# ============================================================================
# Authentication
# ============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ============================================================================
# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
# ============================================================================
LANGUAGE_CODE = FETCH_INTERNATIONALIZATION.language_code
TIME_ZONE = FETCH_INTERNATIONALIZATION.time_zone
USE_I18N = FETCH_INTERNATIONALIZATION.use_i18n
USE_TZ = FETCH_INTERNATIONALIZATION.use_tz


# ============================================================================
# Runcommands
# ============================================================================
RUNINSTALL = FETCH_RUNCOMMANDS.install
RUNBUILD = FETCH_RUNCOMMANDS.build


# ============================================================================
# Layout
# ============================================================================
ALWAYS_SHOW_ADMIN = FETCH_LAYOUT.always_show_admin
LAYOUT = FETCH_LAYOUT.option
