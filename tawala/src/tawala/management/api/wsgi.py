"""[FETCH_PROJECT_IMPORT_ALLOWED] WSGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/wsgi
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
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
