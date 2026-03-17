"""Internationalization Configuration.

https://docs.djangoproject.com/en/stable/topics/i18n/
"""

from ..conf import BaseConf, ConfField

__all__: list[str] = ["LANGUAGE_CODE", "TIME_ZONE", "USE_I18N", "USE_TZ"]


class _InternationalizationConf(BaseConf):
    """Internationalization Configuration."""

    verbose_name = "05. Internationalization Configuration"

    language_code = ConfField(type=str, env="LANGUAGE_CODE", toml="internationalization.language_code", default="en-us")
    time_zone = ConfField(type=str, env="TIME_ZONE", toml="internationalization.time_zone", default="Africa/Nairobi")
    use_i18n = ConfField(type=bool, env="USE_I18N", toml="internationalization.use_i18n", default=True)
    use_tz = ConfField(type=bool, env="USE_TZ", toml="internationalization.use_tz", default=True)


_INTERNATIONALIZATION = _InternationalizationConf()

LANGUAGE_CODE = _INTERNATIONALIZATION.language_code
TIME_ZONE = _INTERNATIONALIZATION.time_zone
USE_I18N = _INTERNATIONALIZATION.use_i18n
USE_TZ = _INTERNATIONALIZATION.use_tz
