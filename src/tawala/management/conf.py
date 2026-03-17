"""Configuration field descriptors and base settings class."""

import builtins
import pathlib
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Final, TypeAlias, cast

from christianwhocodes import InitAction, PyProject

from ..constants import Package


class ProjectValidationError(Exception):
    """Current directory is not a valid project."""


@dataclass(frozen=True)
class _ProjectConf:
    """Project configuration for the current working directory."""

    _validated: bool = field(default=False, init=False, repr=False)
    _toml: dict[str, Any] = field(default_factory=lambda: dict(), init=False, repr=False)
    _base_dir: pathlib.Path = field(default_factory=pathlib.Path.cwd)

    def _load_project(self) -> None:
        """Load and validate pyproject.toml configuration."""
        pyproject_path = self._base_dir / "pyproject.toml"
        if not pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at '{pyproject_path}'")
        tool_section = PyProject(pyproject_path).data.get("tool", {})
        if Package.NAME not in tool_section:
            raise KeyError(f"Missing 'tool.{Package.NAME}' section in pyproject.toml")
        object.__setattr__(self, "_toml", tool_section[Package.NAME])

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


PROJECT_CONF: Final = _ProjectConf()

_ConfDefaultValueType: TypeAlias = str | bool | list[str] | pathlib.Path | int | None


class ConfField:
    """Descriptor for a configuration field populated from env vars or TOML."""

    def __init__(
        self,
        type: type[str] | type[bool] | type[list[str]] | type[pathlib.Path] | type[int] = str,
        choices: list[str] | None = None,
        env: str | None = None,
        toml: str | None = None,
        default: _ConfDefaultValueType = None,
    ):
        """Set up field type, source mappings, and default value."""
        self.type = type
        self.choices = choices
        self.env = env
        self.toml = toml
        self.default = default
        self.field_name: str = ""

    # ============================================================================
    # Value Resolution
    # ============================================================================

    def _get_from_toml(self) -> Any:
        """Get value from TOML configuration."""
        if self.toml is None:
            return None
        current: Any = PROJECT_CONF.toml
        for k in self.toml.split("."):
            if isinstance(current, dict) and k in current:
                current = cast(dict[str, Any], current)[k]
            else:
                return None
        return current

    def _fetch_value(self) -> Any:
        """Fetch configuration value with fallback priority: ENV -> TOML -> default."""
        # Try environment variable first
        if self.env is not None and self.env in PROJECT_CONF.env:
            return PROJECT_CONF.env[self.env]
        # Fall back to TOML config
        toml_value = self._get_from_toml()
        if toml_value is not None:
            return toml_value
        # Final fallback to default
        return self.default

    # ============================================================================
    # Value Conversion
    # ============================================================================

    @staticmethod
    def convert_value(value: Any, target_type: Any, field_name: str | None = None) -> _ConfDefaultValueType:
        """Convert a raw value to the target type."""
        from christianwhocodes import TypeConverter

        if value is None:
            match target_type:
                case builtins.str:
                    return ""
                case builtins.int:
                    return 0
                case builtins.list:
                    return []
                case _:
                    return None
        try:
            match target_type:
                case builtins.str:
                    return str(value)
                case builtins.int:
                    return int(value)
                case builtins.list:
                    return TypeConverter.to_list_of_str(value, str.strip)
                case builtins.bool:
                    return TypeConverter.to_bool(value)
                case pathlib.Path:
                    return TypeConverter.to_path(value)
                case _:
                    raise ValueError(f"Unsupported target type or type not specified: {target_type}")
        except ValueError as e:
            field_info = f" for field '{field_name}'" if field_name else ""
            raise ValueError(f"Error converting config value{field_info}: {e}") from e

    # ============================================================================
    # Descriptor Protocol
    # ============================================================================

    def __set_name__(self, owner: type, name: str) -> None:
        """Capture the attribute name when the descriptor is assigned to a class."""
        self.field_name = name

    def __get__(self, instance: Any, owner: type) -> Any:
        """Fetch, convert, and return the configuration value."""
        if instance is None:
            return self
        raw_value = self._fetch_value()
        return self.convert_value(raw_value, self.type, self.field_name)


class BaseConf:
    """Base class for loading settings from env vars and TOML."""

    verbose_name: str

    # Track all Conf subclasses
    _subclasses: list[type["BaseConf"]] = []

    def __init_subclass__(cls) -> None:
        """Register subclass and collect env field metadata."""
        super().__init_subclass__()
        BaseConf._subclasses.append(cls)  # Register this subclass

        # Initialize _env_fields for this subclass
        if not hasattr(cls, "_env_fields"):
            cls._env_fields: list[dict[str, Any]] = []

        for attr_value in vars(cls).values():
            if not isinstance(attr_value, ConfField):
                continue

            # Store field metadata
            # if attr_value.env is not None:
            cls._env_fields.append(
                {
                    "class": cls.verbose_name,
                    "choices": attr_value.choices,
                    "env": attr_value.env,
                    "toml": attr_value.toml,
                    "default": attr_value.default,
                    "type": attr_value.type,
                }
            )

    @classmethod
    def get_conf_fields(cls) -> list[dict[str, Any]]:
        """Collect all ConfField definitions."""
        env_fields: list[dict[str, Any]] = []
        for subclass in cls._subclasses:
            if hasattr(subclass, "_env_fields"):
                env_fields.extend(subclass._env_fields)
        return sorted(env_fields, key=lambda f: f["class"])  # Sort by class name for better organization
