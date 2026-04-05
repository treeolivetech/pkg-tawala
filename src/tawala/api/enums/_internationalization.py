from enum import StrEnum

__all__ = ["InternationalizationTomlKeys"]


class InternationalizationTomlKeys(StrEnum):
    """Keys for internationalization configuration in pyproject.toml."""

    MAIN = "internationalization"
    LANGUAGE_CODE = "language-code"
    TIME_ZONE = "time-zone"
    USE_I18N = "use-i18n"
    USE_TZ = "use-tz"
