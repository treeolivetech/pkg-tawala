"""Core urls."""

from typing import TypeAlias

from django.apps import apps
from django.conf import settings, urls
from django.contrib import admin
from django.urls import URLPattern as DjURLPattern
from django.urls import URLResolver, include, path
from django.views.generic.base import TemplateView
from tawala_api.conf.enums import LayoutOptions

URLPattern: TypeAlias = DjURLPattern | URLResolver
urlpatterns: list[URLPattern]

match settings.LAYOUT:
    case LayoutOptions.WIP.value:
        urlpatterns = [path("", include(f"{settings.LAYOUTS_MODULE}.wip.urls"))]
    case _:
        urlpatterns = [path("", include(f"{settings.MAIN_APP}.urls"))]

urlpatterns += [
    *(
        [path("widgets/logout/", include(f"{settings.WIDGETS_MODULE}.logout.urls"))]
        if apps.is_installed(f"{settings.WIDGETS_MODULE}.logout")
        else []
    ),
    *(
        [path("admin/", admin.site.urls)]
        if (settings.ALWAYS_SHOW_ADMIN and apps.is_installed("django.contrib.admin"))
        else []
    ),
    *(
        [path("__reload__/", include("django_browser_reload.urls"))]
        if apps.is_installed("django_browser_reload")
        else []
    ),
]

urls.handler404 = TemplateView.as_view(template_name="core/404.html")
