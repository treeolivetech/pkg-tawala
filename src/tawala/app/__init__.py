"""ASGI & WSGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/asgi
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi
"""

from os import environ

from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application

from .. import Package

environ.setdefault("DJANGO_SETTINGS_MODULE", Package.SETTINGS_MODULE)

asgi_application = get_asgi_application()
wsgi_application = get_wsgi_application()
