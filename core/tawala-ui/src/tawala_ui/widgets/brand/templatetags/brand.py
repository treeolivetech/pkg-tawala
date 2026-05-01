"""Brand template tags."""

from typing import Any, cast

from django import template
from django.utils.safestring import SafeString, mark_safe

from ..models import (
    Icon,
    IconChoice,
    Logo,
    LogoVariantChoice,
    Name,
    NameChoice,
    Description,
    DescriptionChoice,
)

register = template.Library()


# ==============================================
# Name tags
# ==============================================
@register.simple_tag
def brand_name(name_type: str = NameChoice.FULL_NAME) -> str:
    """Return the brand name value for the given NameChoice type.

    Usage:
        {% brand_name %}                          → full name (default)
        {% brand_name "short_name" %}             → short name
        {% brand_name as my_var %}                → stored in variable
    """
    try:
        return cast(Any, Name).objects.get(type=name_type).data
    except cast(Any, Name).DoesNotExist:
        return ""


@register.simple_tag
def brand_full_name() -> str:
    """Shortcut for {% brand_name "full_name" %}."""
    return brand_name(NameChoice.FULL_NAME)


@register.simple_tag
def brand_short_name() -> str:
    """Shortcut for {% brand_name "short_name" %}."""
    return brand_name(NameChoice.SHORT_NAME)


@register.simple_tag
def brand_legal_name() -> str:
    """Shortcut for {% brand_name "legal_name" %}."""
    return brand_name(NameChoice.LEGAL_NAME)


@register.simple_tag
def brand_description(description_type: str = DescriptionChoice.SHORT) -> str:
    """Return the brand description value for the given DescriptionChoice type.

    Usage:
        {% brand_description %}                       → short description (default)
        {% brand_description "long" %}                → long description
        {% brand_description as my_var %}             → stored in variable
    """
    try:
        return cast(Any, Description).objects.get(type=description_type).data
    except cast(Any, Description).DoesNotExist:
        return ""


@register.simple_tag
def brand_short_description() -> str:
    """Shortcut for {% brand_description "short" %}."""
    return brand_description(DescriptionChoice.SHORT)


@register.simple_tag
def brand_long_description() -> str:
    """Shortcut for {% brand_description "long" %}."""
    return brand_description(DescriptionChoice.LONG)


@register.simple_tag
def brand_mission_statement() -> str:
    """Shortcut for {% brand_description "mission_statement" %}."""
    return brand_description(DescriptionChoice.MISSION_STATEMENT)


@register.simple_tag
def brand_vision_statement() -> str:
    """Shortcut for {% brand_description "vision_statement" %}."""
    return brand_description(DescriptionChoice.VISION_STATEMENT)


# ==============================================
# Icon tags
# ==============================================
@register.simple_tag
def brand_icon(icon_type: str = IconChoice.FAVICON_ICO) -> str:
    """Return the icon URL for the given IconChoice type.

    Usage:
        {% brand_icon %}                          → favicon.ico (default)
        {% brand_icon "favicon_svg" %}            → SVG favicon
        {% brand_icon "apple_touch_icon" %}       → Apple touch icon
        {% brand_icon as my_var %}                → stored in variable
    """
    try:
        return cast(Any, Icon).objects.get(name=icon_type).data
    except cast(Any, Icon).DoesNotExist:
        return ""


def _versioned_url(url: str, version: str) -> str:
    """Append a cache-busting query string to a URL if a version is given."""
    return f"{url}?v={version}" if version else url


@register.simple_tag
def brand_favicon_ico_html(version: str = "") -> SafeString:
    """Return a full <link> tag for the .ico favicon.

    Usage:
        {% brand_favicon_ico_html %}
        {% brand_favicon_ico_html "20260427" %}
    """
    url = _versioned_url(brand_icon(IconChoice.FAVICON_ICO), version)
    return mark_safe(f'<link rel="shortcut icon" type="image/x-icon" href="{url}" />')


@register.simple_tag
def brand_favicon_svg_html(version: str = "") -> SafeString:
    """Return a full <link> tag for the .svg favicon.

    Usage:
        {% brand_favicon_svg_html %}
        {% brand_favicon_svg_html "20260427" %}
    """
    url = _versioned_url(brand_icon(IconChoice.FAVICON_SVG), version)
    return mark_safe(f'<link rel="icon" type="image/svg+xml" href="{url}" />')


@register.simple_tag
def brand_apple_touch_icon_html(version: str = "") -> SafeString:
    """Return a full <link> tag for the Apple Touch Icon.

    Usage:
        {% brand_apple_touch_icon_html %}
        {% brand_apple_touch_icon_html "20260427" %}
    """
    url = _versioned_url(brand_icon(IconChoice.APPLE_TOUCH_ICON), version)
    return mark_safe(f'<link rel="apple-touch-icon" sizes="180x180" href="{url}" />')


# ==============================================
# Logo tags
# ==============================================
@register.simple_tag
def brand_logo(variant: str = LogoVariantChoice.LIGHT) -> str:
    """Return the logo URL for the given LogoVariantChoice.

    Usage:
        {% brand_logo %}                          → light variant (default)
        {% brand_logo "dark" %}                   → dark variant
        {% brand_logo "colorless" %}              → colorless variant
        {% brand_logo as my_var %}                → stored in variable
    """
    try:
        return cast(Any, Logo).objects.get(name=variant).data
    except cast(Any, Logo).DoesNotExist:
        return ""


@register.simple_tag
def primary_logo() -> str:
    """Return the URL of the primary active logo, with graceful fallbacks.

    Falls back to the first active logo if no primary is set.

    Usage:
        from ..management.api import Description, DescriptionChoice
        {% primary_logo %}
        {% primary_logo as logo_url %}
    """
    LogoObjects = cast(Any, Logo)

    logo = LogoObjects.objects.filter(is_primary=True, is_active=True).first()
    if logo:
        return logo.data  # type: ignore[no-any-return]

    logo = LogoObjects.objects.filter(is_active=True).order_by("display_order").first()
    return logo.data if logo else ""  # type: ignore[no-any-return]
