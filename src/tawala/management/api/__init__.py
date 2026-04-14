from os import environ  # noqa: D104

from ... import CONF

environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"{CONF.pkg_name}.management.conf.post",
)
