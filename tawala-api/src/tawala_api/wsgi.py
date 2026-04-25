"""[FETCH_PROJECT_IMPORT_ALLOWED] WSGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/wsgi
"""

from sys import exit

from .conf import (
    DJANGO_SETTINGS_MODULE,
    FETCH_PROJECT,
    FetchProjectValidationError,
    print_invalid_project_help,
)

try:
    FETCH_PROJECT.validate_project()
except FetchProjectValidationError as e:
    exit(print_invalid_project_help(e))
except Exception as e:
    from christianwhocodes import ExitCode, Text, cprint

    cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
    exit(ExitCode.ERROR)
else:
    from os import environ

    from django.core.wsgi import get_wsgi_application

    environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    application = get_wsgi_application()
