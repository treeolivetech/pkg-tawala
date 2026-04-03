"""base settings."""

from ... import DefaultApps, Package, Project

__all__ = ["BASE_DIR", "ROOT_URLCONF", "PKG_DISPLAY_NAME"]

PKG_DISPLAY_NAME = Package.DISPLAY_NAME
BASE_DIR = Project.BASE_DIR
ROOT_URLCONF: str = f"{DefaultApps.APP}.urls"
