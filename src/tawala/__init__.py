"""Configuration utilities."""

from functools import cached_property
from pathlib import Path
from typing import Any, Final

from christianwhocodes import PyProject, Version

__all__ = ["ConfValidationError", "CONF"]


class ConfValidationError(Exception):
    """Raised when the project directory or config is invalid."""

    def __init__(
        self,
        message: str = "Project directory could not be loaded. Ensure the project is validated.",
    ) -> None:
        """Initialize the validation error with a default message."""
        super().__init__(message)


class _Conf:
    """Project configuration, lazily loaded from pyproject.toml."""

    def __init__(self) -> None:
        """Initialize project configuration for a specific package."""
        self._validated = False
        self._base_toml: dict[str, Any] = {}
        self._base_dir: Path | None = None

        self.pkg_name: Final[str] = "tawala"
        self.pkg_display_name: Final[str] = self.pkg_name.capitalize()
        self.pkg_version: Final[str] = Version.get(self.pkg_name)[0]
        self.alias: Final[str] = "twl"

    def _load_project(self) -> None:
        """Load and validate pyproject.toml configuration."""
        pyproject_path = Path.cwd() / "pyproject.toml"
        if not pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at '{pyproject_path}'")
        tool_section = PyProject(pyproject_path).data.get("tool", {})
        if self.pkg_name not in tool_section:
            raise KeyError(f"Missing 'tool.{self.pkg_name}' section in pyproject.toml")
        self._base_toml = tool_section[self.pkg_name]
        self._base_dir = pyproject_path.parent

    def validate_project(self) -> None:
        """Validate the project once; subsequent calls are no-ops."""
        if self._validated:
            return
        try:
            self._load_project()
        except (FileNotFoundError, KeyError) as e:
            raise ConfValidationError(str(e)) from e
        self._validated = True

    @cached_property
    def base_toml(self) -> dict[str, Any]:
        """pyproject.toml config section for this package (lazy-loaded)."""
        self.validate_project()
        return self._base_toml

    @cached_property
    def base_dir(self) -> Path:
        """Root directory containing pyproject.toml (lazy-loaded)."""
        self.validate_project()
        assert self._base_dir is not None  # guaranteed after validate()
        return self._base_dir

    @cached_property
    def base_env(self) -> dict[str, Any]:
        """Merged .env file and process environment variables (lazy-loaded)."""
        from os import environ

        from dotenv import dotenv_values

        return {**dotenv_values(self.base_dir / ".env"), **environ}

    @cached_property
    def base_name(self) -> str:
        """Project name derived from the project directory name (lazy-loaded)."""
        return self.base_dir.name


CONF = _Conf()
"""Singleton instance of configuration and validation utilities."""
