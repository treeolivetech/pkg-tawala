"""Core urls."""

from typing import TypeAlias

from django.apps import apps
from django.conf import settings, urls
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic.base import TemplateView
from tawala_school.apps import SCHOOL_APP
from tawala_ui.apps import WIDGET_LOGOUT
from tawala_wip.apps import WIP_APP

URLPatterns: TypeAlias = list[URLPattern | URLResolver]

# ------------------------------------------------------------------------

urlpatterns: URLPatterns = [
    *(
        [path("__logout__/", LogoutView.as_view(), name="widget_logout")]
        if apps.is_installed(WIDGET_LOGOUT)
        else []
    ),
    *([path("admin/", admin.site.urls)] if settings.SHOW_ADMIN_IN_PRODUCTION else []),
]

# ------------------------------------------------------------------------

_dashboard_urlpattern: URLPatterns = [
    path("", include(f"{settings.DASHBOARD_APP}.urls"))
]

urlpatterns.extend([
    *(
        [path("", include(f"{WIP_APP}.urls"))]
        if apps.is_installed(WIP_APP)
        else _dashboard_urlpattern
    ),
    *(
        [path("", include(f"{SCHOOL_APP}.urls"))]
        if apps.is_installed(SCHOOL_APP)
        else _dashboard_urlpattern
    ),
])

# ------------------------------------------------------------------------

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
else:
    urls.handler404 = TemplateView.as_view(template_name="base/404.html")
