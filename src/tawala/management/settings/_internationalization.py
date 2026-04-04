"""Internationalization Configuration.

https://docs.djangoproject.com/en/stable/topics/i18n/
"""

from ..enums import InternationalizationTomlKeys
from .conf import Conf, ConfField

__all__ = ["LANGUAGE_CODE", "TIME_ZONE", "USE_I18N", "USE_TZ"]

# ============================================================================
# Configuration fields
# ============================================================================


class _InternationalizationConf(Conf):
    """Internationalization Configuration."""

    verbose_name = "Internationalization Configuration"

    language_code = ConfField(
        type=str,
        env="LANGUAGE_CODE",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.LANGUAGE_CODE}",
        default="en-us",
    )
    time_zone = ConfField(
        type=str,
        env="TIMEZONE",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.TIME_ZONE}",
        default="UTC",
    )
    use_i18n = ConfField(
        type=bool,
        env="USE_I18N",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.USE_I18N}",
        default=True,
    )
    use_tz = ConfField(
        type=bool,
        env="USE_TZ",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.USE_TZ}",
        default=True,
    )


_INTERNATIONALIZATION = _InternationalizationConf()


# ============================================================================
# Public variables
# ============================================================================

LANGUAGE_CODE = _INTERNATIONALIZATION.language_code

TIME_ZONE = _INTERNATIONALIZATION.time_zone

USE_I18N = _INTERNATIONALIZATION.use_i18n

USE_TZ = _INTERNATIONALIZATION.use_tz
