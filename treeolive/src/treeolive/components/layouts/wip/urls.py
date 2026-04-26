"""Layout Work In Progress URLs."""

from django.urls import path

from .views import WorkInProgressLayout

urlpatterns = [
    path("", WorkInProgressLayout.as_view(), name="layout_wip"),
]
