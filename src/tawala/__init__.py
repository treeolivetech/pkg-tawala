# noqa: D104
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any, Final

from christianwhocodes import InitAction, PyProject, Version

__all__ = ["ProjectValidationError", "Package", "PROJECT"]


class ProjectValidationError(Exception):
    """Current directory is not a valid project."""


class Package:
    """Package/Project metadata."""

    NAME: Final[str] = Path(__file__).parent.resolve().name
    DISPLAY_NAME: Final[str] = NAME.capitalize()
    VERSION: Final[str] = Version.get(NAME)[0]
    SETTINGS_MODULE: Final[str] = f"{NAME}.management.settings"
    MAIN_APP: Final[str] = f"{NAME}.app"


@dataclass(frozen=True)
class _Project:
    """configuration for the current working directory."""

    _validated: bool = field(default=False, init=False, repr=False)
    _toml: dict[str, Any] = field(default_factory=lambda: {}, init=False, repr=False)
    _base_dir: Path = field(default_factory=Path.cwd)

    def _load_project(self) -> None:
        """Load and validate pyproject.toml configuration."""
        pyproject_path = self._base_dir / "pyproject.toml"
        pkg_name = Package.NAME
        if not pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at '{pyproject_path}'")
        tool_section = PyProject(pyproject_path).data.get("tool", {})
        if pkg_name not in tool_section:
            raise KeyError(f"Missing 'tool.{pkg_name}' section in pyproject.toml")
        object.__setattr__(self, "_toml", tool_section[pkg_name])

    @cached_property
    def toml(self) -> dict[str, Any]:
        """pyproject.toml configuration (lazy-loaded)."""
        self.validate()
        return self._toml

    @cached_property
    def env(self) -> dict[str, Any]:
        """Combined .env and environment variables (lazy-loaded)."""
        self.validate()
        from os import environ

        from dotenv import dotenv_values

        return {**dotenv_values(self._base_dir / ".env"), **environ}

    @cached_property
    def base_dir(self) -> Path:
        """Base directory (lazy-loaded)."""
        self.validate()
        return self._base_dir

    @cached_property
    def home_app(self) -> str:
        """Home app name."""
        return "home"

    def validate(self) -> None:
        """Check if the current directory is a valid project. Runs once.

        In CLI, we catch the exception for pretty printing.
        In Production, this will bubble up to the WSGI/ASGI server.
        """
        if self._validated:
            return
        from sys import argv

        if any(arg in argv for arg in InitAction):  # Avoid validation during startproject commands
            object.__setattr__(self, "_validated", True)
            return
        try:
            self._load_project()
        except (FileNotFoundError, KeyError) as e:
            raise ProjectValidationError(str(e)) from e
        else:
            object.__setattr__(self, "_validated", True)


PROJECT: Final = _Project()
