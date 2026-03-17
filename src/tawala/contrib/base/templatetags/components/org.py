"""Organization component template tags."""

# from django import template
# from django.templatetags.static import static

# from ..settings import ORG
# from ..types import OrgKey

# register = template.Library()


# @register.simple_tag
# def org(key: OrgKey) -> str:
#     """Return the organization name."""
#     try:
#         org_key = key.lower().replace("-", "_")

#         match org_key:
#             case "logo_url" | "favicon_url" | "apple_touch_icon_url":
#                 return static(getattr(ORG, org_key, ""))
#             case _:
#                 return getattr(ORG, org_key, "")

#     except (AttributeError, KeyError):
#         return ""
