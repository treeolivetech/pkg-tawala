"""API backend (ASGI/WSGI)."""

from os import environ

from ....constants import Package
from ...settings import SERVER_USE_ASGI
from ._asgi import asgi_application
from ._wsgi import wsgi_application

environ.setdefault("DJANGO_SETTINGS_MODULE", Package.SETTINGS_MODULE)

__all__: list[str] = ["server_application", "asgi_application", "wsgi_application"]

server_application = asgi_application if SERVER_USE_ASGI else wsgi_application
