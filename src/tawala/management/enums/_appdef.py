from enum import StrEnum

__all__ = [
    "MainAppTomlKeys",
    "MainAppOptions",
    "MainAppFlags",
    "RuncommandsTomlKeys",
    "InternationalizationTomlKeys",
]


# ============================================================================
# Main App
# ============================================================================


class MainAppTomlKeys(StrEnum):
    """Keys for security configuration in pyproject.toml."""

    MAIN = "main-app"


class MainAppOptions(StrEnum):
    """Keys for security configuration in pyproject.toml."""

    HOME = "home"


class MainAppFlags(StrEnum):
    """Flags used when setting up database during initialization."""

    APP = "--app"


# ============================================================================
# Runcommands
# ============================================================================
class RuncommandsTomlKeys(StrEnum):
    """Keys for storage configuration in pyproject.toml."""

    MAIN = "runcommands"
    INSTALL = "install"
    BUILD = "build"


# ============================================================================
# Internationalization
# ============================================================================
class InternationalizationTomlKeys(StrEnum):
    """Keys for internationalization configuration in pyproject.toml."""

    MAIN = "internationalization"
    LANGUAGE_CODE = "language-code"
    TIME_ZONE = "time-zone"
    USE_I18N = "use-i18n"
    USE_TZ = "use-tz"
