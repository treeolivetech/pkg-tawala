"""UI Configuration."""

from christianwhocodes import Version

# --------------------------------------------

_UI_APP = "tawala_ui"
UI_NAME = "tawala-ui"
UI_VERSION = Version.get(UI_NAME)[0]

# --------------------------------------------

WIDGETS_LITERAL = "widgets"
WIDGETS_MODULE = f"{_UI_APP}.{WIDGETS_LITERAL}"

WIDGET_ADDRESSES = f"{WIDGETS_MODULE}.addresses"
WIDGET_BRAND = f"{WIDGETS_MODULE}.brand"
WIDGET_LISTS = f"{WIDGETS_MODULE}.lists"
WIDGET_FOOTER = f"{WIDGETS_MODULE}.footer"
WIDGET_HEADER = f"{WIDGETS_MODULE}.header"
WIDGET_SCROLL_TOP = f"{WIDGETS_MODULE}.scroll_top"
WIDGET_PRELOADER = f"{WIDGETS_MODULE}.preloader"
WIDGET_LOGOUT = f"{WIDGETS_MODULE}.logout"

WIDGET_APPS = [
    WIDGET_ADDRESSES,
    WIDGET_BRAND,
    WIDGET_LISTS,
    WIDGET_FOOTER,
    WIDGET_HEADER,
    WIDGET_SCROLL_TOP,
    WIDGET_PRELOADER,
    WIDGET_LOGOUT,
]

# --------------------------------------------

ASSETS_LITERAL = "assets"
ASSETS_MODULE = f"{_UI_APP}.{ASSETS_LITERAL}"

ASSET_AOS = f"{ASSETS_MODULE}.aos"
ASSET_BOOTSTRAP = f"{ASSETS_MODULE}.bootstrap"

ASSET_APPS = [ASSET_AOS, ASSET_BOOTSTRAP]

# --------------------------------------------

UI_APPS = WIDGET_APPS + ASSET_APPS
