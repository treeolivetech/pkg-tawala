from enum import StrEnum

__all__ = ["RuncommandsTomlKeys"]


class RuncommandsTomlKeys(StrEnum):
    """Keys for storage configuration in pyproject.toml."""

    MAIN = "runcommands"
    INSTALL = "install"
    BUILD = "build"
