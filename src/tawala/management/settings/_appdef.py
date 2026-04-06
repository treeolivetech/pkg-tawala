from typing import cast

from ... import Package
from ..configs import INTERNATIONALIZATION_CONF, MAIN_APP_CONF, RUNCOMMANDS_CONF
from ..typings import TemplatesDict

__all__ = [
    "ROOT_URLCONF",
    "ASGI_APPLICATION",
    "WSGI_APPLICATION",
    "MAIN_APP",
    "INSTALLED_APPS",
    "MIDDLEWARE",
    "TEMPLATES",
    "STATICFILES_FINDERS",
    "SASS_PRECISION",
    "AUTH_PASSWORD_VALIDATORS",
    "RUNINSTALL",
    "RUNBUILD",
    "LANGUAGE_CODE",
    "TIME_ZONE",
    "USE_I18N",
    "USE_TZ",
]

# ============================================================================
# Root URL Conf
# ============================================================================

ROOT_URLCONF = f"{Package.APP}.urls"

# ============================================================================
# Asgi & Wsgi
# ============================================================================

ASGI_APPLICATION = f"{Package.MANAGEMENT}.asgi.application"

WSGI_APPLICATION = f"{Package.MANAGEMENT}.wsgi.application"

# ============================================================================
# Main app
# ============================================================================

MAIN_APP = cast(str, MAIN_APP_CONF.name)


# ============================================================================
# Installed app
# ============================================================================

INSTALLED_APPS = (
    [
        "django_browser_reload",
        "django_watchfiles",
        "django_minify_html",
        "django_http_compression",
        "sass_processor",
    ]
    + [MAIN_APP, Package.APP, Package.NAME]
    + [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
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
# Templates
# ============================================================================

TEMPLATES: TemplatesDict = [
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
# Staticfiles & Sass
# ============================================================================

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

SASS_PRECISION = 8


# ============================================================================
# Authentication
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ============================================================================
# Runcommands
# ============================================================================

RUNINSTALL = RUNCOMMANDS_CONF.install

RUNBUILD = RUNCOMMANDS_CONF.build


# ============================================================================
# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
# ============================================================================

LANGUAGE_CODE = INTERNATIONALIZATION_CONF.language_code

TIME_ZONE = INTERNATIONALIZATION_CONF.time_zone

USE_I18N = INTERNATIONALIZATION_CONF.use_i18n

USE_TZ = INTERNATIONALIZATION_CONF.use_tz
