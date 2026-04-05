from ..enums import RuncommandsTomlKeys
from ._startproject import Conf, ConfField

__all__ = ["RUNCOMMANDS"]


# ============================================================================
# Configuration fields
# ============================================================================


class _RunCommandsConf(Conf):
    """Runcommands Configuration."""

    verbose_name = "Runcommands Configuration"

    install = ConfField(
        type=list,
        env="RUNCOMMANDS_INSTALL",
        toml=f"{RuncommandsTomlKeys.MAIN}.{RuncommandsTomlKeys.INSTALL}",
        default=[],
    )
    build = ConfField(
        type=list,
        env="RUNCOMMANDS_BUILD",
        toml=f"{RuncommandsTomlKeys.MAIN}.{RuncommandsTomlKeys.BUILD}",
        default=["makemigrations", "migrate", "compilescss", "collectstatic --noinput --ignore=*.scss"],
    )


# ============================================================================
# Public variables
# ============================================================================


RUNCOMMANDS = _RunCommandsConf()
