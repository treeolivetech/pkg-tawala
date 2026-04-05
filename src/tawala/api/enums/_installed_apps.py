from enum import StrEnum

__all__ = ["AppTomlKeys"]


class AppTomlKeys(StrEnum):
    """Keys for security configuration in pyproject.toml."""

    MAIN_APP = "main-app"
