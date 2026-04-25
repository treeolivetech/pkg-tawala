"""Apps urls."""

from typing import TypeAlias

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern as DjURLPattern
from django.urls import URLResolver, include, path
from tawala_api.conf import LayoutOptions

URLPattern: TypeAlias = DjURLPattern | URLResolver

urlpatterns: list[URLPattern] = [
    path("__reload__/", include("django_browser_reload.urls")),
    *([path("admin/", admin.site.urls)] if settings.ALWAYS_SHOW_ADMIN else []),
    path("registration/", include("django.contrib.auth.urls")),
]

match settings.LAYOUT:
    case LayoutOptions.WIP.value:
        urlpatterns += [path("", include(f"{settings.LAYOUTS_MODULE}.wip.urls"))]
    case _:
        urlpatterns += [path("", include(f"{settings.MAIN_APP}.urls"))]
