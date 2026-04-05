"""Security and Deployment Configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
https://docs.djangoproject.com/en/stable/howto/csp/
"""

from django.utils.csp import CSP  # pyright: ignore[reportMissingTypeStubs]

from ..enums import SecurityTomlKeys
from ._startproject import Conf, ConfField

__all__ = [
    "SECRET_KEY",
    "DEBUG",
    "ALLOWED_HOSTS",
    "SECURE_SSL_REDIRECT",
    "SESSION_COOKIE_SECURE",
    "CSRF_COOKIE_SECURE",
    "SECURE_HSTS_SECONDS",
    "WORK_IN_PROGRESS",
    "SECURE_CSP",
]


# ============================================================================
# Configuration fields
# ============================================================================


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


_SECURITY = _SecurityConf()

# ============================================================================
# Public variables
# ============================================================================


SECRET_KEY = _SECURITY.secret_key

DEBUG = _SECURITY.debug

ALLOWED_HOSTS = _SECURITY.allowed_hosts

SECURE_SSL_REDIRECT = _SECURITY.secure_ssl_redirect

SESSION_COOKIE_SECURE = _SECURITY.session_cookie_secure

CSRF_COOKIE_SECURE = _SECURITY.csrf_cookie_secure

SECURE_HSTS_SECONDS = _SECURITY.secure_hsts_seconds

WORK_IN_PROGRESS = _SECURITY.wip

SECURE_CSP: dict[str, list[str]] = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE],
    "style-src": [
        CSP.SELF,
        CSP.NONCE,
        "https://fonts.googleapis.com",  # Google Fonts CSS
    ],
    "font-src": [
        CSP.SELF,
        "https://fonts.gstatic.com",  # Google Fonts font files
    ],
}
