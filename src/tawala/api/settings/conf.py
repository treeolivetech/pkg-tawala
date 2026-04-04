"""management."""

import builtins
import pathlib
from typing import Any, TypeAlias, cast

from ... import PROJECT

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
        current: Any = PROJECT.toml
        for k in self.toml.split("."):
            if isinstance(current, dict) and k in current:
                current = cast(dict[str, Any], current)[k]
            else:
                return None
        return current

    def _fetch_value(self) -> Any:
        """Fetch configuration value with fallback priority: ENV -> TOML -> default."""
        # Try environment variable first
        if self.env is not None and self.env in PROJECT.env:
            return PROJECT.env[self.env]
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

        # This point should not be reachable; added to avoid implicit None return.
        raise ValueError(f"Unsupported target type or conversion failure for: {target_type}")

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


class Conf:
    """Base class for loading configuration from env vars and TOML."""

    verbose_name: str

    # Track all Conf subclasses
    _subclasses: list[type["Conf"]] = []

    def __init_subclass__(cls) -> None:
        """Register subclass and collect env field metadata."""
        super().__init_subclass__()
        Conf._subclasses.append(cls)  # Register this subclass

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
