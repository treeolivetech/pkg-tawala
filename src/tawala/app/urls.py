"""URL configuration for the WIP app."""

from django.conf import settings
from django.urls import URLPattern, URLResolver, include, path, re_path

from .. import DjangoApps, Project, VendorApps
from .views import WIPView

# Initialize the base URL patterns list
urlpatterns: list[URLPattern | URLResolver] = []

# Django browser reload should be placed before the WIP catch-all
# to ensure the development server can auto-reload the WIP page.
if VendorApps.BROWSER_RELOAD in settings.INSTALLED_APPS:
    urlpatterns.append(path("__reload__/", include(f"{VendorApps.BROWSER_RELOAD}.urls")))

if settings.WORK_IN_PROGRESS:
    # Catch-all route for WIP mode: everything not matched above goes to the WIP page.
    urlpatterns.append(re_path(r"^.*$", WIPView.as_view(), name="wip_catchall"))
else:
    # Optional URL additions loaded when NOT in WIP mode
    if DjangoApps.AUTH in settings.INSTALLED_APPS:
        urlpatterns.append(path("registration/", include(f"{DjangoApps.AUTH}.urls")))

    # The main application routes
    urlpatterns += [path("", include(f"{Project.HOME_APP_NAME}.urls"))]
