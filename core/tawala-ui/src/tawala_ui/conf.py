"""UI Configuration."""

from christianwhocodes import Version

# --------------------------------------------

UI_APP = "tawala_ui"
UI_NAME = "tawala-ui"
UI_VERSION = Version.get(UI_NAME)[0]

# --------------------------------------------

_WIDGETS_MODULE = f"{UI_APP}.widgets"

WIDGET_ADDRESSES = f"{_WIDGETS_MODULE}.addresses"
WIDGET_LISTS = f"{_WIDGETS_MODULE}.lists"
WIDGET_FOOTER = f"{_WIDGETS_MODULE}.footer"
WIDGET_HEADER = f"{_WIDGETS_MODULE}.header"
WIDGET_SCROLL_TOP = f"{_WIDGETS_MODULE}.scroll_top"
WIDGET_PRELOADER = f"{_WIDGETS_MODULE}.preloader"

WIDGET_APPS = [
    WIDGET_ADDRESSES,
    WIDGET_LISTS,
    WIDGET_FOOTER,
    WIDGET_HEADER,
    WIDGET_SCROLL_TOP,
    WIDGET_PRELOADER,
]

# --------------------------------------------

_ASSETS_MODULE = f"{UI_APP}.assets"

ASSET_AOS = f"{_ASSETS_MODULE}.aos"
ASSET_BOOTSTRAP = f"{_ASSETS_MODULE}.bootstrap"

ASSET_APPS = [ASSET_AOS, ASSET_BOOTSTRAP]

# --------------------------------------------

UI_APPS = WIDGET_APPS + ASSET_APPS
