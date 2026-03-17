"""Middleware Configuration."""

from ...constants import AppDefMappings, Middlewares
from ..conf import BaseConf, ConfField
from ._07_installed_apps import INSTALLED_APPS

__all__: list[str] = ["MIDDLEWARE"]


class _MiddlewareConf(BaseConf):
    """Middleware Configuration."""

    verbose_name = "08. Middleware Configuration"

    extend = ConfField(type=list, env="MIDDLEWARE_EXTEND", toml="middleware.extend", default=[])
    remove = ConfField(type=list, env="MIDDLEWARE_REMOVE", toml="middleware.remove", default=[])


_MIDDLEWARE_CONF = _MiddlewareConf()


def _get_middleware(installed_apps: list[str]) -> list[str]:
    """Build the final MIDDLEWARE list based on installed apps."""
    middlewares: list[Middlewares] = [m for m in Middlewares]

    # Collect middleware that should be removed based on missing apps
    middleware_to_remove: set[str] = set(_MIDDLEWARE_CONF.remove)
    for app, middleware_list in AppDefMappings.APP_MIDDLEWARE.items():
        if app not in installed_apps:
            middleware_to_remove.update(middleware_list)

    # Filter out middleware whose apps are not installed or explicitly removed
    middlewares = [m for m in middlewares if m not in middleware_to_remove]

    # Add custom middleware at the end (before browser reload if it exists)
    all_middleware: list[str] = middlewares + _MIDDLEWARE_CONF.extend

    # Remove duplicates while preserving order
    return list(dict.fromkeys(all_middleware))


MIDDLEWARE: list[str] = _get_middleware(INSTALLED_APPS)
