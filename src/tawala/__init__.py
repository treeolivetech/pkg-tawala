"""Package."""

from pathlib import Path
from typing import Final

from christianwhocodes import Version

__all__ = ["Package"]


class Package:
    """Package/Project metadata."""

    NAME: Final[str] = Path(__file__).parent.name
    DISPLAY_NAME: Final[str] = NAME.capitalize()
    VERSION: Final[str] = Version.get(NAME)[0]
    APP: Final[str] = f"{NAME}.app"
    API: Final[str] = f"{NAME}.api"
    SETTINGS_MODULE: Final[str] = f"{API}.settings"
