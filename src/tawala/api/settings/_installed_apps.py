from typing import cast

from ... import Package
from ..enums import AppTomlKeys
from ._startproject import Conf, ConfField

__all__ = ["MAIN_APP", "INSTALLED_APPS", "ROOT_URLCONF", "ASGI_APPLICATION", "WSGI_APPLICATION"]

# ============================================================================
# Configuration fields
# ============================================================================


class _AppConf(Conf):
    """Main App Configuration."""

    verbose_name = "Main App Configuration"

    main_app = ConfField(
        type=str,
        env="MAIN_APP",
        toml=AppTomlKeys.MAIN_APP,
        default="home",
    )


# ============================================================================
# Public variables
# ============================================================================

MAIN_APP = cast(str, _AppConf().main_app)

INSTALLED_APPS = (
    [
        "django_browser_reload",
        "django_watchfiles",
        "django_minify_html",
        "django_http_compression",
        "whitenoise.runserver_nostatic",
        "sass_processor",
    ]
    + [MAIN_APP, Package.APP, Package.API]
    + [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
)

ROOT_URLCONF = f"{Package.APP}.urls"

ASGI_APPLICATION = f"{Package.API}.asgi.application"

WSGI_APPLICATION = f"{Package.API}.wsgi.application"
