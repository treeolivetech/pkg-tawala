"""Installed Apps Configuration."""

from ... import DefaultApps, DjangoApps, VendorApps
from .. import ConfField, SettingsConf

__all__ = ["INSTALLED_APPS"]


class _AppsConf(SettingsConf):
    """Installed Apps Configuration."""

    verbose_name = "06. Installed Apps Configuration"

    extend = ConfField(type=list, env="APPS_EXTEND", toml="apps.extend", default=[])
    remove = ConfField(type=list, env="APPS_REMOVE", toml="apps.remove", default=[])


_APPS_CONF = _AppsConf()


def _get_installed_apps() -> list[str]:
    """Build the final INSTALLED_APPS list."""
    apps_first_in_the_list: list[VendorApps] = [a for a in VendorApps]
    apps_middle_of_the_list: list[DefaultApps] = _APPS_CONF.extend + [
        a for a in DefaultApps
    ]
    apps_last_in_the_list: list[DjangoApps] = [a for a in DjangoApps]

    # Collect apps that should be removed except those in `apps_middle_of_the_list`
    apps_to_remove = [
        app for app in _APPS_CONF.remove if app not in apps_middle_of_the_list
    ]

    # Filter apps to be removed from `apps_first_in_the_list` and `apps_last_in_the_list`
    apps_first_in_the_list = [
        app for app in apps_first_in_the_list if app not in apps_to_remove
    ]
    apps_last_in_the_list = [
        app for app in apps_last_in_the_list if app not in apps_to_remove
    ]

    # Return all apps while removing duplicates
    return list(
        dict.fromkeys(
            apps_first_in_the_list + apps_middle_of_the_list + apps_last_in_the_list
        )
    )


INSTALLED_APPS: list[str] = _get_installed_apps()
