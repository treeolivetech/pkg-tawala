"""[PROJECT_CONF_IMPORT_ALLOWED_PREINIT] WSGI configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/wsgi
"""

from sys import exit

from christianwhocodes import ExitCode, Text, cprint

from ...settings.conf import PROJECT_CONF, BaseValidationError

try:
    PROJECT_CONF.validate_project()
except BaseValidationError as e:
    cprint(
        f"Is this a valid {PROJECT_CONF.pkg_display_name} project directory?\n{e}",
        Text.WARNING,
    )
    cprint(
        f"Assuming you have uv installed:\n"
        f"    - run: 'uvx {PROJECT_CONF.cli_pkg_name} new <project_name>' to initialize a new project.\n"
        f"    - run: 'uvx {PROJECT_CONF.cli_pkg_name} -h' to see help on the command.",
        Text.INFO,
    )
    exit(ExitCode.ERROR)
except Exception as e:
    cprint(f"Unexpected error during project validation:\n{e}", Text.ERROR)
    exit(ExitCode.ERROR)
else:
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
