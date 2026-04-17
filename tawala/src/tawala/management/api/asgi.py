"""[FETCH_PROJECT_IMPORT_ALLOWED] ASGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/asgi
"""

from sys import exit

from ..settings.fetch import FETCH_PROJECT, FetchProjectValidationError

try:
    FETCH_PROJECT.validate_project()
except FetchProjectValidationError as e:
    from . import print_invalid_project_help

    exit(print_invalid_project_help(e))
except Exception as e:
    from christianwhocodes import ExitCode, Text, cprint

    cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
    exit(ExitCode.ERROR)
else:
    from django.core.asgi import get_asgi_application

    application = get_asgi_application()
