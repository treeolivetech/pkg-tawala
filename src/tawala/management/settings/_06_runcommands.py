"""Runcommands Configuration."""

from ..conf import BaseConf, ConfField

__all__: list[str] = ["RUNCOMMANDS"]


class _RunCommandsConf(BaseConf):
    """Runcommands Configuration."""

    verbose_name = "06. Runcommands Configuration"

    install = ConfField(type=list, env="RUNCOMMANDS_INSTALL", toml="runcommands.install", default=[])
    build = ConfField(
        type=list,
        env="RUNCOMMANDS_BUILD",
        toml="runcommands.build",
        default=["makemigrations", "migrate", "compilescss", "collectstatic --noinput --ignore=*.scss"],
    )


RUNCOMMANDS = _RunCommandsConf()
