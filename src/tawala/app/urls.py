"""URL configuration."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeAlias

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern as BaseURLPattern
from django.urls import URLResolver, include, path, re_path

from .views import WIPView

URLPattern: TypeAlias = BaseURLPattern | URLResolver
_URLFactory: TypeAlias = Callable[[], URLPattern]


@dataclass
class _URLEntry:
    """Represents a conditional URL configuration entry."""

    condition: bool
    factory: _URLFactory


_URL_ENTRIES: list[_URLEntry] = [
    _URLEntry(
        condition="django_browser_reload" in settings.INSTALLED_APPS,
        factory=lambda: path("__reload__/", include("django_browser_reload.urls")),
    ),
    _URLEntry(
        condition="django.contrib.admin" in settings.INSTALLED_APPS,
        factory=lambda: path("admin/", admin.site.urls),
    ),
    _URLEntry(
        condition="django.contrib.auth" in settings.INSTALLED_APPS,
        factory=lambda: path("registration/", include("django.contrib.auth.urls")),
    ),
]

urlpatterns = [entry.factory() for entry in _URL_ENTRIES if entry.condition] + (
    [re_path(r"^.*$", WIPView.as_view(), name="wip_catchall")]
    if settings.WORK_IN_PROGRESS
    else [path("", include(f"{settings.MAIN_APP}.urls"))]
)
