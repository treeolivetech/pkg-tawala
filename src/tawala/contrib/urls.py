"""URL configuration."""

from django.conf import settings
from django.urls import URLPattern, URLResolver, include, path

from ..constants import InstalledApps, Project

urlpatterns: list[URLPattern | URLResolver] = [
    *(
        [path("__reload__/", include(f"{InstalledApps.BROWSER_RELOAD}.urls"))]
        if InstalledApps.BROWSER_RELOAD in settings.INSTALLED_APPS
        else []
    ),
    *([path("registration/", include(f"{InstalledApps.AUTH}.urls"))] if InstalledApps.AUTH in settings.INSTALLED_APPS else []),
    path("", include(f"{Project.HOME_APP_NAME}.urls")),
]
