"""Installed Apps Configuration."""

from ...constants import InstalledApps, Package, Project
from ..conf import BaseConf, ConfField

__all__: list[str] = ["INSTALLED_APPS"]


class _AppsConf(BaseConf):
    """Installed Apps Configuration."""

    verbose_name = "07. Installed Apps Configuration"

    extend = ConfField(type=list, env="APPS_EXTEND", toml="apps.extend", default=[])
    remove = ConfField(type=list, env="APPS_REMOVE", toml="apps.remove", default=[])


_APPS_CONF = _AppsConf()


def _get_installed_apps() -> list[str]:
    """Build the final INSTALLED_APPS list."""
    apps_first_in_the_list: list[InstalledApps] = [
        InstalledApps.BROWSER_RELOAD,
        InstalledApps.WATCHFILES,
        InstalledApps.MINIFY_HTML,
        InstalledApps.HTTP_COMPRESSION,
    ]
    apps_middle_of_the_list: list[InstalledApps | str] = _APPS_CONF.extend + [Project.HOME_APP_NAME, Package.NAME]
    apps_last_in_the_list: list[InstalledApps] = [
        InstalledApps.SASS_PROCESSOR,
        InstalledApps.ADMIN,
        InstalledApps.AUTH,
        InstalledApps.CONTENTTYPES,
        InstalledApps.SESSIONS,
        InstalledApps.MESSAGES,
        InstalledApps.STATICFILES,
    ]

    # Collect apps that should be removed except those in `apps_middle_of_the_list`
    apps_to_remove = [app for app in _APPS_CONF.remove if app not in apps_middle_of_the_list]

    # Filter apps to be removed from `apps_first_in_the_list` and `apps_last_in_the_list`
    apps_first_in_the_list = [app for app in apps_first_in_the_list if app not in apps_to_remove]
    apps_last_in_the_list = [app for app in apps_last_in_the_list if app not in apps_to_remove]

    # Return all apps while removing duplicates
    return list(dict.fromkeys(apps_first_in_the_list + apps_middle_of_the_list + apps_last_in_the_list))


INSTALLED_APPS: list[str] = _get_installed_apps()
