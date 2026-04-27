"""Core urls."""

from typing import TypeAlias

from django.apps import apps
from django.conf import settings, urls
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic.base import TemplateView
from tawala_school.conf import SCHOOL_APP
from tawala_wip.conf import WIP_APP

URLPatterns: TypeAlias = list[URLPattern | URLResolver]

_auth_logout_urlpattern: URLPatterns = [
    path("__logout__/", LogoutView.as_view(), name="auth_logout"),
]

_dashboard_urlpattern: URLPatterns = [
    path("", include(f"{settings.DASHBOARD_APP}.urls"))
]

urlpatterns: URLPatterns = [
    *([path("admin/", admin.site.urls)] if settings.SHOW_ADMIN_IN_PRODUCTION else []),
    *(
        [path("", include(f"{WIP_APP}.urls"))]
        if apps.is_installed(WIP_APP)
        else _dashboard_urlpattern
    ),
    *(
        [path("", include(f"{SCHOOL_APP}.urls"))]
        if apps.is_installed(SCHOOL_APP)
        else _auth_logout_urlpattern + _dashboard_urlpattern
    ),
    path("__reload__/", include("django_browser_reload.urls")),
]

urls.handler404 = TemplateView.as_view(template_name="base/404.html")
