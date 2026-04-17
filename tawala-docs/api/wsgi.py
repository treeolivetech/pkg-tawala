"""WSGI entrypoint for the tawala-docs project."""

from tawala.management.api.wsgi import application

app = application
