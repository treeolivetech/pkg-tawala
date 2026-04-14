"""[BASE_CONF_IMPORT_ALLOWED_PREINIT] Management api."""

from os import environ

from ...settings.conf import BASE_CONF

# TODO: Test if this will work on Vercel. If not, first try using a function that sets it, then call the function in the other required modules. If it still doesn't work, try using lambdas, and it that doesn't work, just set it manually in the other modules. The goal is to avoid repeating this line in multiple modules if possible, but it may be necessary if the environment variable needs to be set before importing any api module.

environ.setdefault("DJANGO_SETTINGS_MODULE", f"{BASE_CONF.pkg_name}.settings.main")
