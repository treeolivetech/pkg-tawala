"""Generate Configuration."""

from ..conf import BaseConf

__all__: list[str] = ["CONF_FIELDS"]

CONF_FIELDS = BaseConf.get_conf_fields()
