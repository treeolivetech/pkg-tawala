"""Work in Progress urls."""

from django.conf import settings
from django.urls import re_path

from .views import WorkInProgressLayout

urlpatterns = (
    [re_path(r"^.*$", WorkInProgressLayout.as_view(), name="wip_catchall")]
    if settings.LAYOUT_WIP
    else []
)
