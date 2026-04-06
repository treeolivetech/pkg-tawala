"""Security and Deployment Configuration.

https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
https://docs.djangoproject.com/en/stable/howto/csp/
"""

from django.utils.csp import CSP  # pyright: ignore[reportMissingTypeStubs]

from ..configs import SECURITY_CONF

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

SECRET_KEY = SECURITY_CONF.secret_key

DEBUG = SECURITY_CONF.debug

ALLOWED_HOSTS = SECURITY_CONF.allowed_hosts

SECURE_SSL_REDIRECT = SECURITY_CONF.secure_ssl_redirect

SESSION_COOKIE_SECURE = SECURITY_CONF.session_cookie_secure

CSRF_COOKIE_SECURE = SECURITY_CONF.csrf_cookie_secure

SECURE_HSTS_SECONDS = SECURITY_CONF.secure_hsts_seconds

WORK_IN_PROGRESS = SECURITY_CONF.wip

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
