"""WSGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/wsgi
"""

from os import environ

from django.core.wsgi import get_wsgi_application

from .. import Package

environ.setdefault("DJANGO_SETTINGS_MODULE", Package.SETTINGS_MODULE)

application = get_wsgi_application()
