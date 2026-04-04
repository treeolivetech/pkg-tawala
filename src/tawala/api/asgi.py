"""ASGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/asgi
"""

from os import environ

from django.core.asgi import get_asgi_application

from .. import Package

environ.setdefault("DJANGO_SETTINGS_MODULE", Package.SETTINGS_MODULE)

application = get_asgi_application()
