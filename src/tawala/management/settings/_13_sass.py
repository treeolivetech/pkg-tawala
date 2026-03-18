"""Sass Configuration."""

from ...constants import InstalledApps
from ._07_installed_apps import INSTALLED_APPS

if InstalledApps.SASS_PROCESSOR in INSTALLED_APPS:
    __all__ = ["SASS_PRECISION"]

    SASS_PRECISION = 8
else:
    __all__ = []
