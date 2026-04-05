from enum import StrEnum

__all__ = ["AppTomlKeys", "RuncommandsTomlKeys", "InternationalizationTomlKeys"]


class AppTomlKeys(StrEnum):
    """Keys for security configuration in pyproject.toml."""

    MAIN_APP = "main-app"


class RuncommandsTomlKeys(StrEnum):
    """Keys for storage configuration in pyproject.toml."""

    MAIN = "runcommands"
    INSTALL = "install"
    BUILD = "build"


class InternationalizationTomlKeys(StrEnum):
    """Keys for internationalization configuration in pyproject.toml."""

    MAIN = "internationalization"
    LANGUAGE_CODE = "language-code"
    TIME_ZONE = "time-zone"
    USE_I18N = "use-i18n"
    USE_TZ = "use-tz"
