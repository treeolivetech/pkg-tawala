from enum import StrEnum

__all__ = ["SecurityTomlKeys"]


class SecurityTomlKeys(StrEnum):
    """Keys for security configuration in pyproject.toml."""

    WORK_IN_PROGRESS = "work-in-progress"
    SECRET_KEY = "secret-key"
    DEBUG = "debug"
    ALLOWED_HOSTS = "allowed-hosts"
    SECURE_SSL_REDIRECT = "secure-ssl-redirect"
    SESSION_COOKIE_SECURE = "session-cookie-secure"
    CSRF_COOKIE_SECURE = "csrf-cookie-secure"
    SECURE_HSTS_SECONDS = "secure-hsts-seconds"
