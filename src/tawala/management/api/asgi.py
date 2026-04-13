"""ASGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/asgi
"""

from sys import exit

from christianwhocodes import ExitCode, Text, cprint

from ... import CONF, ConfValidationError

try:
    CONF.validate_project()
except ConfValidationError as e:
    cprint(
        f"Is this a valid {CONF.pkg_display_name} project directory?\n{e}",
        Text.WARNING,
    )
    cprint(
        f"Assuming you have uv installed:\n"
        f"    - run: 'uvx {CONF.pkg_name} startproject <project_name>' to initialize a new project.\n"
        f"    - run: 'uvx {CONF.pkg_name} startproject -h' to see help on the command.",
        Text.INFO,
    )
    exit(ExitCode.ERROR)
except Exception as e:
    cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
    exit(ExitCode.ERROR)
else:
    from django.core.asgi import get_asgi_application

    application = get_asgi_application()
