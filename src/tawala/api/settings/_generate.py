"""Generate Configuration."""

from .conf import Conf

__all__ = ["CONF_FIELDS"]

CONF_FIELDS = Conf.get_conf_fields()
