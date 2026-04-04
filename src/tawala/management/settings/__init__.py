"""Settings configuration."""

from pathlib import Path
from typing import NotRequired, TypeAlias, TypedDict

from ... import PROJECT, Package
from ._databases import *
from ._internationalization import *
from ._runcommands import *
from ._security import *
from ._storages import *

"""Comes last so as to generate files with the above configurations."""
from ._generate import *

# ============================================================================
# Typed dictionaries
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


TemplatesDict: TypeAlias = list[_TemplateDict]


# ============================================================================
# Public variables
# ============================================================================

# Application entry points
ROOT_URLCONF = f"{Package.MAIN_APP}.urls"
ASGI_APPLICATION = f"{Package.MAIN_APP}.asgi_application"
WSGI_APPLICATION = f"{Package.MAIN_APP}.wsgi_application"

# Installed apps
_THIRD_PARTY_APPS = [
    "django_browser_reload",
    "django_watchfiles",
    "django_minify_html",
    "django_http_compression",
    "whitenoise.runserver_nostatic",
    "sass_processor",
]

_PROJECT_APPS = [PROJECT.home_app, Package.MAIN_APP, Package.NAME]

_DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = _THIRD_PARTY_APPS + _PROJECT_APPS + _DJANGO_APPS

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

# Templates
_TEMPLATE_CONTEXT_PROCESSORS = [
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.template.context_processors.csp",
]

# TODO: Create an inbuilt template tag called pkg_display_name
TEMPLATES: TemplatesDict = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": _TEMPLATE_CONTEXT_PROCESSORS},
    }
]

# Authentication
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Static files and SASS
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

SASS_PRECISION = 8
