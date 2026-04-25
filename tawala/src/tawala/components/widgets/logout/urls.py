"""Widget logout urls."""

from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path("", LogoutView.as_view(), name="widget_logout"),
]
