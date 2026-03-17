"""Contact info component template tags."""

# from typing import Literal

# from django import template

# from ..settings import CONTACTINFO_ADDRESS, CONTACTINFO_EMAIL, CONTACTINFO_PHONE
# from ..types import ContactAddressKey, ContactEmailKey, ContactPhoneKey

# register = template.Library()


# @register.simple_tag
# def contactinfo_address(key: ContactAddressKey | Literal["full"]) -> str:
#     """Returns the specified address field from contact address setting."""

#     contactinfo_address = CONTACTINFO_ADDRESS

#     if key == "full":
#         address_parts: list[str | None] = [
#             contactinfo_address.street,
#             contactinfo_address.city,
#             contactinfo_address.state,
#             contactinfo_address.country,
#         ]
#         return ", ".join(filter(None, address_parts))

#     return getattr(contactinfo_address, key, "")


# @register.simple_tag
# def contactinfo_email(key: ContactEmailKey | Literal["all"] = "primary") -> str | list[str]:
#     """Returns the specified email field from contact email setting."""

#     contactinfo_email = CONTACTINFO_EMAIL

#     if key == "all":
#         emails: list[str] = []
#         if contactinfo_email.primary:
#             emails.append(contactinfo_email.primary)
#         if contactinfo_email.additional:
#             emails.extend(contactinfo_email.additional)
#         return emails

#     if key == "additional":
#         return contactinfo_email.additional or []

#     return contactinfo_email.primary or ""


# @register.simple_tag
# def contactinfo_phone(key: ContactPhoneKey | Literal["all"] = "primary") -> str | list[str]:
#     """Returns the specified phone field from contact phone setting."""

#     contactinfo_phone = CONTACTINFO_PHONE

#     if key == "all":
#         phones: list[str] = []
#         if contactinfo_phone.primary:
#             phones.append(contactinfo_phone.primary)
#         if contactinfo_phone.additional:
#             phones.extend(contactinfo_phone.additional)
#         return phones

#     if key == "additional":
#         return contactinfo_phone.additional or []

#     return contactinfo_phone.primary or ""


# @register.inclusion_tag("contactinfo/address_block.html")
# def contactinfo_address_block() -> dict[str, str]:
#     """Renders a formatted address block."""

#     contactinfo_address = CONTACTINFO_ADDRESS

#     return {
#         "street": contactinfo_address.street,
#         "city": contactinfo_address.city,
#         "state": contactinfo_address.state,
#         "country": contactinfo_address.country,
#     }


# @register.inclusion_tag("contactinfo/email_list.html")
# def contactinfo_email_list() -> dict[str, list[str]]:
#     """Renders a list of all email addresses."""

#     contactinfo_email = CONTACTINFO_EMAIL

#     emails: list[str] = []
#     if contactinfo_email.primary:
#         emails.append(contactinfo_email.primary)
#     if contactinfo_email.additional:
#         emails.extend(contactinfo_email.additional)
#     return {"emails": emails}


# @register.inclusion_tag("contactinfo/phone_list.html")
# def contactinfo_phone_list() -> dict[str, list[str]]:
#     """Renders a list of all phone numbers."""

#     contactinfo_phone = CONTACTINFO_PHONE

#     phones: list[str] = []
#     if contactinfo_phone.primary:
#         phones.append(contactinfo_phone.primary)
#     if contactinfo_phone.additional:
#         phones.extend(contactinfo_phone.additional)
#     return {"phones": phones}
