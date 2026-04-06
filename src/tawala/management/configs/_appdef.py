from ..enums import AppTomlKeys, InternationalizationTomlKeys, RuncommandsTomlKeys
from ._utils import Conf, ConfField

__all__ = ["MAIN_APP_CONF", "RUNCOMMANDS_CONF", "INTERNATIONALIZATION_CONF"]

# ============================================================================
# Main app
# ============================================================================


class _MainAppConf(Conf):
    """Main App Configuration."""

    verbose_name = "Main App Configuration"

    name = ConfField(
        type=str,
        env="MAIN_APP",
        toml=AppTomlKeys.MAIN_APP,
        default="home",
    )


MAIN_APP_CONF = _MainAppConf()


# ============================================================================
# Runcommands
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


RUNCOMMANDS_CONF = _RunCommandsConf()


# ============================================================================
# Internationalization
# ============================================================================


class _InternationalizationConf(Conf):
    """Internationalization Configuration."""

    verbose_name = "Internationalization Configuration"

    language_code = ConfField(
        type=str,
        env="LANGUAGE_CODE",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.LANGUAGE_CODE}",
        default="en-us",
    )
    time_zone = ConfField(
        type=str,
        env="TIMEZONE",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.TIME_ZONE}",
        default="UTC",
    )
    use_i18n = ConfField(
        type=bool,
        env="USE_I18N",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.USE_I18N}",
        default=True,
    )
    use_tz = ConfField(
        type=bool,
        env="USE_TZ",
        toml=f"{InternationalizationTomlKeys.MAIN}.{InternationalizationTomlKeys.USE_TZ}",
        default=True,
    )


INTERNATIONALIZATION_CONF = _InternationalizationConf()
