from enum import StrEnum

__all__ = ["StartprojectPresetChoices", "StartprojectPresetInitFlags"]


class StartprojectPresetChoices(StrEnum):
    """Available database backends."""

    DEFAULT = "default"
    VERCEL = "vercel"


class StartprojectPresetInitFlags(StrEnum):
    """Flags used when setting up preset during initialization."""

    PRESET = "--preset"
