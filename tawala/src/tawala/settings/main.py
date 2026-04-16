"""[BASE_CONF_IMPORT_ALLOWED_PREINIT] Main settings."""

from pathlib import Path
from typing import NotRequired, TypeAlias, TypedDict

from django.utils.csp import CSP  # pyright: ignore[reportMissingTypeStubs]

from .conf import (
    BASE_CONF,
    DATABASES_CONF,
    INTERNATIONALIZATION_CONF,
    LAYOUT_CONF,
    PRESETS_CONF,
    RUNCOMMANDS_CONF,
    SECURITY_CONF,
)
from .enums import DatabaseOptions, LayoutOptions, PresetOptions

# ============================================================================
# Core
# ============================================================================
PKG_NAME = BASE_CONF.pkg_name
PKG_DISPLAY_NAME = BASE_CONF.pkg_display_name
PKG_VERSION = BASE_CONF.pkg_version
BASE_DIR = BASE_CONF.base_dir


# ============================================================================
# Security & Deployment
# https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
# https://docs.djangoproject.com/en/stable/howto/csp/
# ============================================================================
SECRET_KEY = SECURITY_CONF.secret_key
DEBUG = SECURITY_CONF.debug_option
ALLOWED_HOSTS = SECURITY_CONF.allowed_hosts
SECURE_SSL_REDIRECT = SECURITY_CONF.secure_ssl_redirect
SESSION_COOKIE_SECURE = SECURITY_CONF.session_cookie_secure
CSRF_COOKIE_SECURE = SECURITY_CONF.csrf_cookie_secure
SECURE_HSTS_SECONDS = SECURITY_CONF.secure_hsts_seconds

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
# Installed applications
# ============================================================================
MAIN_APP = "app"

INSTALLED_APPS = (
    [
        "django_browser_reload",
        "django_minify_html",
        "django_http_compression",
    ]
    + [MAIN_APP]
    + [
        f"{PKG_NAME}.apps.layouts.wip",
        f"{PKG_NAME}.apps.layouts.base",
        f"{PKG_NAME}.apps.widgets.preloader",
        f"{PKG_NAME}.apps.widgets.scroll_top",
        f"{PKG_NAME}.apps.vendors.bootstrap",
        f"{PKG_NAME}.apps.vendors.aos",
    ]
    + [PKG_NAME]
    + [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "sass_processor",
        "django.contrib.staticfiles",
    ]
)


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
ASGI_APPLICATION = f"{PKG_NAME}.management.api.asgi.application"
WSGI_APPLICATION = f"{PKG_NAME}.management.api.wsgi.application"


# ============================================================================
# Root URLConf
# ============================================================================
ROOT_URLCONF = f"{PKG_NAME}.apps.layouts.base.urls"


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
            ]
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
        case PresetOptions.DEFAULT:
            storage_backend = "django.core.files.storage.FileSystemStorage"
        case PresetOptions.VERCEL:
            storage_backend = (
                f"{PKG_NAME}.management.backends.storage.VercelBlobStorageBackend"
            )
        case _:
            raise ValueError(f"Unsupported storage backend: {preset_option}")

    return {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
        "default": {"BACKEND": storage_backend},
    }


STORAGES = get_storages_config(PRESETS_CONF.option)
BLOB_READ_WRITE_TOKEN = PRESETS_CONF.blob_read_write_token


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
    backend: str = DATABASES_CONF.option.lower()
    match backend:
        case DatabaseOptions.DEFAULT_SQLITE:
            return {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": BASE_DIR / "db.sqlite3",
                }
            }
        case DatabaseOptions.POSTGRESQL:
            config: _DatabaseDict
            if DATABASES_CONF.pg_use_vars:
                config = {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": DATABASES_CONF.pg_database,
                    "USER": DATABASES_CONF.pg_user,
                    "PASSWORD": DATABASES_CONF.pg_password,
                    "HOST": DATABASES_CONF.pg_host,
                    "PORT": str(DATABASES_CONF.pg_port),
                    "OPTIONS": {
                        "pool": DATABASES_CONF.pg_pool,
                        "sslmode": DATABASES_CONF.pg_sslmode,
                    },
                }
            else:
                config = {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": DATABASES_CONF.pg_database,
                    "OPTIONS": {
                        "pool": DATABASES_CONF.pg_pool,
                        "sslmode": DATABASES_CONF.pg_sslmode,
                        "service": DATABASES_CONF.pg_service,
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
LANGUAGE_CODE = INTERNATIONALIZATION_CONF.language_code
TIME_ZONE = INTERNATIONALIZATION_CONF.time_zone
USE_I18N = INTERNATIONALIZATION_CONF.use_i18n
USE_TZ = INTERNATIONALIZATION_CONF.use_tz


# ============================================================================
# Runcommands
# ============================================================================
RUNINSTALL = RUNCOMMANDS_CONF.install
RUNBUILD = RUNCOMMANDS_CONF.build


# ============================================================================
# Layout
# ============================================================================
LAYOUT_ALWAYS_SHOW_ADMIN = LAYOUT_CONF.always_show_admin
LAYOUT_BASE = LAYOUT_CONF.option == LayoutOptions.DEFAULT_BASE
LAYOUT_WIP = LAYOUT_CONF.option == LayoutOptions.WIP
