"""WIP URLs."""

from django.urls import path

from .views import WIPLayout

urlpatterns = [
    path("", WIPLayout.as_view(), name="layout_wip"),
]
