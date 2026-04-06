from ..enums import SecurityTomlKeys
from ._utils import Conf, ConfField

__all__ = ["SECURITY_CONF"]


class _SecurityConf(Conf):
    """Security and Deployment Configuration."""

    verbose_name = "Security and Deployment Configuration"

    secret_key = ConfField(
        type=str,
        env="SECRET_KEY",
        toml=SecurityTomlKeys.SECRET_KEY,
        default="django-insecure-change-me-in-production-via-env-variable",
    )
    debug = ConfField(
        type=bool,
        env="DEBUG",
        toml=SecurityTomlKeys.DEBUG,
        default=True,
    )
    allowed_hosts = ConfField(
        type=list,
        env="ALLOWED_HOSTS",
        toml=SecurityTomlKeys.ALLOWED_HOSTS,
        default=["localhost", "127.0.0.1"],
    )
    secure_ssl_redirect = ConfField(
        type=bool,
        env="SECURE_SSL_REDIRECT",
        toml=SecurityTomlKeys.SECURE_SSL_REDIRECT,
        default=False,
    )
    session_cookie_secure = ConfField(
        type=bool,
        env="SESSION_COOKIE_SECURE",
        toml=SecurityTomlKeys.SESSION_COOKIE_SECURE,
        default=False,
    )
    csrf_cookie_secure = ConfField(
        type=bool,
        env="CSRF_COOKIE_SECURE",
        toml=SecurityTomlKeys.CSRF_COOKIE_SECURE,
        default=False,
    )
    secure_hsts_seconds = ConfField(
        type=int,
        env="SECURE_HSTS_SECONDS",
        toml=SecurityTomlKeys.SECURE_HSTS_SECONDS,
        default=0,
    )
    wip = ConfField(
        type=bool,
        env="WORK_IN_PROGRESS",
        toml=SecurityTomlKeys.WORK_IN_PROGRESS,
        default=False,
    )


SECURITY_CONF = _SecurityConf()
