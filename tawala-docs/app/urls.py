"""URL configuration for tawala-docs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
