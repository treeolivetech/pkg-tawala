"""WIP urls."""

from django.urls import re_path

from .views import WorkInProgressLayout

urlpatterns = [re_path(r"^.*$", WorkInProgressLayout.as_view(), name="wip_catchall")]
