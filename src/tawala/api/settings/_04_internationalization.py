"""Internationalization Configuration.

https://docs.djangoproject.com/en/stable/topics/i18n/
"""

from ... import InternationalizationTomlKeys
from .. import ConfField, SettingsConf

__all__ = ["LANGUAGE_CODE", "TIME_ZONE", "USE_I18N", "USE_TZ"]


class _InternationalizationConf(SettingsConf):
    """Internationalization Configuration."""

    verbose_name = "04. Internationalization Configuration"

    language_code = ConfField(
        type=str,
        env="LANGUAGE_CODE",
        toml="internationalization.language-code",
        default="en-us",
    )
    time_zone = ConfField(
        type=str,
        env="TIMEZONE",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.TIMEZONE}",
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

LANGUAGE_CODE = _INTERNATIONALIZATION.language_code
TIME_ZONE = _INTERNATIONALIZATION.time_zone
USE_I18N = _INTERNATIONALIZATION.use_i18n
USE_TZ = _INTERNATIONALIZATION.use_tz
