"""ASGI entrypoint for the tawala-docs project."""

from tawala.management.api.asgi import application

app = application
