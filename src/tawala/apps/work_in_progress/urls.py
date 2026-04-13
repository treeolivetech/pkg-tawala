from django.conf import settings  # noqa: D100
from django.urls import re_path

from .views import WorkInProgressView

urlpatterns = (
    [re_path(r"^.*$", WorkInProgressView.as_view(), name="wip_catchall")]
    if settings.WORK_IN_PROGRESS
    else []
)
