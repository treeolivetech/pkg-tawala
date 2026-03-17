"""Social media component template tags."""

# from typing import Any

# from django.template import Library

# from ..settings import SOCIAL_PLATFORM_ICONS_MAP, SOCIAL_PLATFORMS, SOCIAL_URLS
# from ..types import SocialKey

# register = Library()


# @register.simple_tag
# def social_url(key: SocialKey) -> str:
#     """
#     Get the social media URL for a given platform.

#     Usage: {% social_url 'facebook' %}

#     Args:
#         platform: The social platform name (e.g., 'facebook', 'twitter-x')

#     Returns:
#         The configured URL for the platform, or empty string if not configured
#     """
#     try:
#         social_platform = key.lower().replace("-", "_")
#         social_urls_conf = SOCIAL_URLS
#         return getattr(social_urls_conf, social_platform, "")
#     except (AttributeError, KeyError):
#         return ""


# @register.simple_tag
# def social_icon(platform: SocialKey) -> str:
#     """
#     Get the Bootstrap icon class for a given social platform.

#     Usage: {% social_icon 'facebook' %}

#     Args:
#         platform: The social platform name

#     Returns:
#         The Bootstrap icon class string
#     """
#     return SOCIAL_PLATFORM_ICONS_MAP.get(platform, "")


# @register.inclusion_tag("social_urls/social_links.html")
# def social_links(css_class: str = "", icon_size: str = "") -> dict[str, Any]:
#     """
#     Render all configured social media links.

#     Usage: {% social_links css_class="my-social-links" icon_size="fs-4" %}

#     Args:
#         css_class: Additional CSS classes for the container
#         icon_size: Bootstrap font size class for icons (e.g., 'fs-4', 'fs-5')

#     Returns:
#         Context dict with social media links data
#     """
#     links: list[dict[str, str]] = []

#     for platform in SOCIAL_PLATFORMS:
#         platform_key = platform.replace("-", "_")
#         social_urls_conf = SOCIAL_URLS

#         url = getattr(social_urls_conf, platform_key, None)

#         if url:
#             links.append(
#                 {
#                     "platform": platform,
#                     "url": url,
#                     "icon": SOCIAL_PLATFORM_ICONS_MAP[platform],
#                     "label": platform.replace("-", " ").title(),
#                 }
#             )

#     return {"links": links, "css_class": css_class, "icon_size": icon_size}


# @register.filter
# def has_social_urls(obj: Any = None) -> bool:
#     """
#     Check if any social media URLs are configured.

#     Usage: {% if ''|has_social_urls %}...{% endif %}

#     Returns:
#         True if at least one social URL is configured
#     """
#     for platform in SOCIAL_PLATFORMS:
#         platform_key = platform.replace("-", "_")
#         social_urls_conf = SOCIAL_URLS

#         if getattr(social_urls_conf, platform_key, None):
#             return True
#     return False
