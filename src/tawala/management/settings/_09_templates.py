"""Template and Context Processors Configuration."""

from pathlib import Path
from typing import NotRequired, TypeAlias, TypedDict

from ...constants import AppDefMappings, ContextProcessors
from ..conf import BaseConf, ConfField
from ._07_installed_apps import INSTALLED_APPS

__all__: list[str] = ["TEMPLATES"]


class _ContextProcessorsConf(BaseConf):
    """Context Processors Configuration."""

    verbose_name = "09. Context Processors Configuration"

    extend = ConfField(type=list, env="CONTEXT_PROCESSORS_EXTEND", toml="context-processors.extend", default=[])
    remove = ConfField(type=list, env="CONTEXT_PROCESSORS_REMOVE", toml="context-processors.remove", default=[])


_CONTEXT_PROCESSORS_CONF = _ContextProcessorsConf()


def _get_context_processors(installed_apps: list[str]) -> list[str]:
    """Build the final context processors list based on installed apps."""
    contrib_context_processors: list[ContextProcessors] = [cp for cp in ContextProcessors]

    # Collect context processors that should be removed based on missing apps
    context_processors_to_remove: set[str] = set(_CONTEXT_PROCESSORS_CONF.remove)
    for app, processor_list in AppDefMappings.APP_CONTEXT_PROCESSOR.items():
        if app not in installed_apps:
            context_processors_to_remove.update(processor_list)

    # Filter out context processors whose apps are not installed or explicitly removed
    contrib_context_processors = [cp for cp in contrib_context_processors if cp not in context_processors_to_remove]

    # Add custom context processors at the end
    all_context_processors: list[str] = _CONTEXT_PROCESSORS_CONF.extend + contrib_context_processors

    # Remove duplicates while preserving order
    return list(dict.fromkeys(all_context_processors))


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
        "OPTIONS": {"context_processors": _get_context_processors(INSTALLED_APPS)},
    }
]
