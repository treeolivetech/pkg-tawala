"""Settings configuration."""

from ... import DefaultApps, Package, Project
from ._01_security import *
from ._02_server import *
from ._03_databases import *
from ._04_storages import *
from ._05_internationalization import *
from ._06_runcommands import *
from ._07_installed_apps import *
from ._08_middleware import *
from ._09_templates import *
from ._10_staticfile_finders import *
from ._11_auth import *
from ._12_generate import *
from ._13_sass import *
from ._14_csp import *

PKG_DISPLAY_NAME = Package.DISPLAY_NAME
BASE_DIR = Project.BASE_DIR
ROOT_URLCONF: str = f"{DefaultApps.APP}.urls"
