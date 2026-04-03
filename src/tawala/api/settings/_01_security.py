"""Security and Deployment Configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
"""

from ... import SecurityTomlKeys
from .. import ConfField, SettingsConf

__all__ = [
    "SECRET_KEY",
    "DEBUG",
    "ALLOWED_HOSTS",
    "SECURE_SSL_REDIRECT",
    "SESSION_COOKIE_SECURE",
    "CSRF_COOKIE_SECURE",
    "SECURE_HSTS_SECONDS",
    "WORK_IN_PROGRESS",
]


class _SecurityConf(SettingsConf):
    """Security and Deployment Configuration."""

    verbose_name = "01. Security and Deployment Configuration"

    secret_key = ConfField(
        type=str, env="SECRET_KEY", toml="secret-key", default="django-insecure-change-me-in-production-via-env-variable"
    )
    debug = ConfField(type=bool, env="DEBUG", toml=SecurityTomlKeys.DEBUG, default=True)
    allowed_hosts = ConfField(type=list, env="ALLOWED_HOSTS", toml="allowed-hosts", default=["localhost", "127.0.0.1"])
    secure_ssl_redirect = ConfField(type=bool, env="SECURE_SSL_REDIRECT", toml="secure-ssl-redirect", default=False)
    session_cookie_secure = ConfField(type=bool, env="SESSION_COOKIE_SECURE", toml="session-cookie-secure", default=False)
    csrf_cookie_secure = ConfField(type=bool, env="CSRF_COOKIE_SECURE", toml="csrf-cookie-secure", default=False)
    secure_hsts_seconds = ConfField(type=int, env="SECURE_HSTS_SECONDS", toml="secure-hsts-seconds", default=0)
    wip = ConfField(type=bool, env="WORK_IN_PROGRESS", toml=SecurityTomlKeys.WIP, default=False)


_SECURITY = _SecurityConf()

SECRET_KEY: str = _SECURITY.secret_key
DEBUG: bool = _SECURITY.debug
ALLOWED_HOSTS: list[str] = _SECURITY.allowed_hosts
SECURE_SSL_REDIRECT: bool = _SECURITY.secure_ssl_redirect
SESSION_COOKIE_SECURE: bool = _SECURITY.session_cookie_secure
CSRF_COOKIE_SECURE: bool = _SECURITY.csrf_cookie_secure
SECURE_HSTS_SECONDS: int = _SECURITY.secure_hsts_seconds
WORK_IN_PROGRESS: bool = _SECURITY.wip
