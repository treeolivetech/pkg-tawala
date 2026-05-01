"""ASGI/WSGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/asgi
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi
"""

from sys import exit

from tawala_api.apps import PROJECT_API, FetchProjectValidationError

try:
    PROJECT_API.validate_project()
except FetchProjectValidationError as e:
    from tawala_api.apps import print_invalid_project_help

    exit(print_invalid_project_help(e))
except Exception as e:
    from christianwhocodes import ExitCode, Text, cprint

    cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
    exit(ExitCode.ERROR)
else:
    from os import environ

    from tawala_api.apps import (
        SECURITY_API,
        SecurityServerOptions,
    )

    from . import DJANGO_SETTINGS_MODULE

    environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

    match SECURITY_API.server_option:
        case SecurityServerOptions.ASGI.value:
            from django.core.asgi import get_asgi_application

            application = get_asgi_application()

        case _:
            from django.core.wsgi import get_wsgi_application

            application = get_wsgi_application()

    server = application
