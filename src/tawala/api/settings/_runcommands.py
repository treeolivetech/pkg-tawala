"""Runcommands Configuration."""

from .conf import Conf, ConfField

__all__ = ["RUNCOMMANDS"]


# ============================================================================
# Configuration fields
# ============================================================================


class _RunCommandsConf(Conf):
    """Runcommands Configuration."""

    verbose_name = "Runcommands Configuration"

    install = ConfField(type=list, env="RUNCOMMANDS_INSTALL", toml="runcommands.install", default=[])
    build = ConfField(
        type=list,
        env="RUNCOMMANDS_BUILD",
        toml="runcommands.build",
        default=["makemigrations", "migrate", "compilescss", "collectstatic --noinput --ignore=*.scss"],
    )


# ============================================================================
# Public variables
# ============================================================================


RUNCOMMANDS = _RunCommandsConf()
