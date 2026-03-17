"""Staticfile Finders Configuration."""

from ...constants import AppDefMappings, StaticFileFinders
from ..conf import BaseConf, ConfField
from ._07_installed_apps import INSTALLED_APPS

__all__: list[str] = ["STATICFILES_FINDERS"]


class _StaticfileFindersConf(BaseConf):
    """Staticfile Finders Configuration."""

    verbose_name = "10. Staticfile Finders Configuration"

    extend = ConfField(type=list, env="STATICFILE_FINDERS_EXTEND", toml="staticfile_finders.extend", default=[])
    remove = ConfField(type=list, env="STATICFILE_FINDERS_REMOVE", toml="staticfile_finders.remove", default=[])


_STATICFILE_FINDERS_CONF = _StaticfileFindersConf()


def _get_staticfile_finders(installed_apps: list[str]) -> list[str]:
    """Build the final STATICFILES_FINDERS list based on installed apps."""
    contrib_staticfile_finders: list[str] = [
        StaticFileFinders.FILESYSTEM,
        StaticFileFinders.APPDIRECTORIES,
        StaticFileFinders.SASS_PROCESSOR,
    ]

    # Collect staticfile finders that should be removed based on missing apps
    finders_to_remove = set(_STATICFILE_FINDERS_CONF.remove)
    for app, staticfile_finders_list in AppDefMappings.APP_STATICFILES_FINDERS.items():
        if app not in installed_apps:
            finders_to_remove.update(staticfile_finders_list)

    # Filter out staticfile finders whose apps are not installed or explicitly removed
    contrib_staticfile_finders = [m for m in contrib_staticfile_finders if m not in finders_to_remove]

    # Add custom staticfile finders at the end (before browser reload if it exists)
    all_staticfile_finders: list[str] = contrib_staticfile_finders + _STATICFILE_FINDERS_CONF.extend

    # Remove duplicates while preserving order
    return list(dict.fromkeys(all_staticfile_finders))


STATICFILES_FINDERS: list[str] = _get_staticfile_finders(INSTALLED_APPS)
