"""Content Security Policy (CSP).

https://docs.djangoproject.com/en/stable/howto/csp/
"""

from django.utils.csp import CSP  # pyright: ignore[reportMissingTypeStubs]

__all__ = ["SECURE_CSP"]

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
