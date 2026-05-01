"""School urls."""

from django.conf import settings
from django.urls import path, include

urlpatterns = [path(f"{settings.LAYOUT}/", include(f"{settings.DASHBOARD_APP}.urls"))]
