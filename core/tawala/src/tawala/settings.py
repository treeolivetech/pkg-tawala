"""Base settings."""

from pathlib import Path
from typing import NotRequired, TypeAlias, TypedDict

from django.utils.csp import CSP
from tawala_api.apps import (
    API_APP,
    DATABASES_API,
    INTERNATIONALIZATION_API,
    LAYOUT_API,
    PRESET_API,
    PROJECT_API,
    RUNCOMMANDS_API,
    SECURITY_API,
    DatabaseOptions,
    LayoutOptions,
    PresetOptions,
)
from tawala_school.apps import SCHOOL_APP
from tawala_ui.apps import (
    ASSET_BOOTSTRAP,
    ASSETS_LITERAL,
    ASSETS_MODULE,
    UI_APPS,
    WIDGET_ADDRESSES,
    WIDGETS_LITERAL,
    WIDGETS_MODULE,
)
from tawala_wip.apps import WIP_APP

# ============================================================================
# Layout
# ============================================================================

LAYOUT = LAYOUT_API.option
DASHBOARD_APP = LAYOUT_API.dashboard

INSTALLED_APPS: list[str] = [
    "django_browser_reload",
    "django_minify_html",
    "django_http_compression",
    DASHBOARD_APP,
]

# --------------------------------------------

BASE_APP = PROJECT_API.pkg_app
BASE_NAME = PROJECT_API.pkg_name
BASE_DISPLAY_NAME = PROJECT_API.pkg_display_name
BASE_VERSION = PROJECT_API.pkg_version
BASE_DIR = PROJECT_API.base_dir

INSTALLED_APPS.append(BASE_APP)

# --------------------------------------------

match LAYOUT:
    case LayoutOptions.WIP.value:
        # This is a minimalistic layout that only uses styling so
        # there's no need to include all UI apps apart from bootstrap for styling
        INSTALLED_APPS.append(WIP_APP)
        INSTALLED_APPS.append(ASSET_BOOTSTRAP)

    # * For other layouts, we recommend that after you append the layout app,
    # * you first extend UI apps, then remove any that are not needed
    # * Example:
    # case LayoutOptions.SOME_LAYOUT.value:
    #     INSTALLED_APPS.append(SOME_LAYOUT_APP)
    #     INSTALLED_APPS.extend(UI_APPS)
    #     INSTALLED_APPS.remove(WIDGET_SOME_WIDGET)  # If not needed by the layout

    case LayoutOptions.SCHOOL.value:
        INSTALLED_APPS.append(SCHOOL_APP)
        INSTALLED_APPS.extend(UI_APPS)

    case _:
        # Include all UI apps by default,
        INSTALLED_APPS.extend(UI_APPS)

# --------------------------------------------

if WIDGET_ADDRESSES in INSTALLED_APPS:
    INSTALLED_APPS.insert(
        INSTALLED_APPS.index(WIDGET_ADDRESSES) + 1, "phonenumber_field"
    )

if ASSET_BOOTSTRAP in INSTALLED_APPS:
    INSTALLED_APPS.insert(INSTALLED_APPS.index(ASSET_BOOTSTRAP) + 1, "sass_processor")
    SASS_PRECISION = 8
    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "sass_processor.finders.CssFinder",
    ]

# --------------------------------------------

INSTALLED_APPS.extend([
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
])

# --------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "django_http_compression.middleware.HttpCompressionMiddleware",  # * Before any that modify html
    "django_minify_html.middleware.MinifyHtmlMiddleware",  # * After http_compression, before HTML modifiers
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]


# --------------------------------------------

WSGI_APPLICATION = f"{BASE_APP}.management.api.application"
ROOT_URLCONF = f"{BASE_APP}.urls"

# --------------------------------------------


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
            "builtins": [f"{API_APP}.templatetags"],
            "libraries": {
                ASSETS_LITERAL: f"{ASSETS_MODULE}.templatetags",
                WIDGETS_LITERAL: f"{WIDGETS_MODULE}.templatetags",
            },
        },
    }
]


# --------------------------------------------

_PUBLIC_DIR = BASE_DIR / "public"

STATIC_ROOT = _PUBLIC_DIR / "static"
MEDIA_ROOT = _PUBLIC_DIR / "media"

STATIC_URL = "static/"
MEDIA_URL = "media/"

# --------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


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
            storage_backend = f"{API_APP}.vercel.storage.VercelBlobStorage"
        case _:
            raise ValueError(f"Unsupported storage backend: {preset_option}")

    return {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
        "default": {"BACKEND": storage_backend},
    }


STORAGES = get_storages_config(PRESET_API.option)
BLOB_READ_WRITE_TOKEN = PRESET_API.blob_read_write_token


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


def _get_databases_config(db_option: str) -> _DatabasesDict:
    """Build the DATABASES setting based on configured backend."""
    config: _DatabaseDict
    match db_option:
        case DatabaseOptions.SQLITE.value:
            config = {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        case DatabaseOptions.POSTGRESQL.value:
            if DATABASES_API.pg_use_vars:
                config = {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": DATABASES_API.pg_database,
                    "USER": DATABASES_API.pg_user,
                    "PASSWORD": DATABASES_API.pg_password,
                    "HOST": DATABASES_API.pg_host,
                    "PORT": str(DATABASES_API.pg_port),
                    "OPTIONS": {
                        "pool": DATABASES_API.pg_pool,
                        "sslmode": DATABASES_API.pg_sslmode,
                    },
                }
            else:
                config = {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": DATABASES_API.pg_database,
                    "OPTIONS": {
                        "pool": DATABASES_API.pg_pool,
                        "sslmode": DATABASES_API.pg_sslmode,
                        "service": DATABASES_API.pg_service,
                    },
                }
        case _:
            raise ValueError(f"Unsupported DB backend: {db_option}")

    return {"default": config}


DATABASES = _get_databases_config(DATABASES_API.option)


# ============================================================================
# Security & Deployment
# https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
# https://docs.djangoproject.com/en/stable/howto/csp/
# ============================================================================

SECRET_KEY = SECURITY_API.secret_key
DEBUG = SECURITY_API.debug_option
ALLOWED_HOSTS = SECURITY_API.allowed_hosts
SECURE_SSL_REDIRECT = SECURITY_API.secure_ssl_redirect
SESSION_COOKIE_SECURE = SECURITY_API.session_cookie_secure
CSRF_COOKIE_SECURE = SECURITY_API.csrf_cookie_secure
SECURE_HSTS_SECONDS = SECURITY_API.secure_hsts_seconds
SHOW_ADMIN_IN_PRODUCTION = DEBUG or SECURITY_API.always_show_admin

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
# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
# ============================================================================

LANGUAGE_CODE = INTERNATIONALIZATION_API.language_code
TIME_ZONE = INTERNATIONALIZATION_API.time_zone
USE_I18N = INTERNATIONALIZATION_API.use_i18n
USE_TZ = INTERNATIONALIZATION_API.use_tz


# ============================================================================
# Runcommands
# ============================================================================

RUNINSTALL = RUNCOMMANDS_API.install
RUNBUILD = RUNCOMMANDS_API.build
