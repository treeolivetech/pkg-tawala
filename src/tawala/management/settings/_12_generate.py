"""Generate Configuration."""

from ..conf import BaseConf

__all__ = ["CONF_FIELDS"]

CONF_FIELDS = BaseConf.get_conf_fields()
