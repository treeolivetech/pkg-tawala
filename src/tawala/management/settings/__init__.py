"""Settings configuration."""

from pathlib import Path

from django.utils.csp import CSP  # pyright: ignore[reportMissingTypeStubs]

from ...constants import Package
from ._01_security import *
from ._02_databases import *
from ._03_storages import *
from ._04_server import *
from ._05_internationalization import *
from ._06_runcommands import *
from ._07_installed_apps import *
from ._08_middleware import *
from ._09_templates import *
from ._10_staticfile_finders import *
from ._11_auth import *
from ._13_sass import *

"""Import last to ensure all confs that use environment variables are set."""
from ._12_generate import *

BASE_DIR = Path.cwd()

ROOT_URLCONF: str = f"{Package.NAME}.contrib.urls"


# ==============================================================================
# Content Security Policy (CSP)
# https://docs.djangoproject.com/en/stable/howto/csp/
# ==============================================================================

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
