"""Address widget models for social, phone, email, and physical contact data."""

from typing import Any, cast

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField  # pyright: ignore
from tawala_api.utils.models import (
    AbstractCreatedAtUpdatedAt,
    AbstractDisplayOrder,
    AbstractIsActiveIsPrimary,
)

from .utils import SocialMediaPlatformChoice


# ==============================================
# Abstract Base Address classes
# ==============================================
class Address(
    AbstractCreatedAtUpdatedAt, AbstractIsActiveIsPrimary, AbstractDisplayOrder
):
    """Shared base for all address records."""

    class Meta(  # noqa: D106
        AbstractCreatedAtUpdatedAt.Meta,
        AbstractIsActiveIsPrimary.Meta,
        AbstractDisplayOrder.Meta,
    ):
        abstract = True


# ==============================================
# Social Address model
# ==============================================
class Social(Address):
    """Stores one social profile username per platform with an auto-generated icon and URL."""

    class Meta(Address.Meta):
        """Meta configuration."""

        ordering = ["display_order", "name"]

    # ------------------------------------------------------------------------

    name = models.CharField(
        max_length=20,
        choices=SocialMediaPlatformChoice.choices,
        unique=True,
        help_text="Select the social platform. Each platform can only be added once.",
    )

    @property
    def display_name(self) -> str:
        """Return the human-friendly platform label from model choices."""
        return str(self.get_name_display())  # type: ignore

    # ------------------------------------------------------------------------

    icon = models.CharField(
        editable=False,
        max_length=50,
        blank=True,
        help_text="Bootstrap icon CSS classes, auto-generated from the selected platform.",
    )
    # * We're not using the AbstractBootstrapIcon model here since it's auto-populated (See 'save' method).
    # * Excluded from the 'SocialMediaAddressForm' in forms.py. Confirm whether this has been done.

    @property
    def icon_html(self) -> str:
        """Return a template-ready icon element for the selected platform."""
        if self.icon:
            return f'<i class="{self.icon}"></i>'
        return ""

    # ------------------------------------------------------------------------

    username = models.CharField(
        max_length=255,
        help_text=(
            "Your handle or username on this platform (e.g. 'johndoe' or 'acme-corp'). "
            "Do not include the full URL — it is built automatically from the platform. "
            "For YouTube and TikTok the '@' prefix is added automatically if omitted."
        ),
    )

    @property
    def url(self) -> str:
        """Return the full profile URL constructed from the platform base URL and username."""
        return SocialMediaPlatformChoice.build_profile_url_for_value(
            str(self.name), str(self.username)
        )

    # ------------------------------------------------------------------------

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Normalise username, auto-populate icon, and build the profile URL before saving.

        - Auto-prepends '@' for platforms that require it (YouTube, TikTok) if
        the user omitted it.
        - Strips a leading '@' for all other platforms to keep storage clean.
        - Populates the ``icon`` field from the selected platform.
        """
        platform_value = str(self.name)

        # Normalise the username: ensure correct '@' handling.
        username = str(cast(Any, self).username).strip()
        if SocialMediaPlatformChoice.uses_at_prefix_for_value(platform_value):
            if not username.startswith("@"):
                username = f"@{username}"
        else:
            username = username.lstrip("@")

        cast(Any, self).username = username
        cast(Any, self).icon = SocialMediaPlatformChoice.icon_for_value(platform_value)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return a string representation of the Social address."""
        return f"{self.display_name} - {self.url}"


# ==============================================
# Phone Address model
# ==============================================
class Phone(Address):
    """Stores phone contact numbers with optional primary designation."""

    _PhoneNumberModelField: Any = PhoneNumberField

    class Meta(Address.Meta):
        """Meta configuration."""

        ordering = ["display_order", "number"]

    # ------------------------------------------------------------------------

    number = _PhoneNumberModelField(
        region="KE",
        help_text="Phone number in Kenyan local or international format (e.g., 0712345678 or +254712345678).",
        unique=True,
    )

    @property
    def national_format(self) -> str:
        """Return the number in national format (e.g., 0712 345678)."""
        return str(getattr(self.number, "as_national", ""))

    @property
    def international_format(self) -> str:
        """Return the number in international format (e.g., +254 712 345678)."""
        return str(getattr(self.number, "as_international", ""))

    @property
    def tel_link(self) -> str:
        """Return an RFC 3966 tel URI (e.g., tel:+254-712-345678)."""
        return str(getattr(self.number, "as_rfc3966", ""))

    # ------------------------------------------------------------------------

    @property
    def whatsapp_link(self) -> str:
        """Return a wa.me URL for the active primary number."""
        if self.is_primary and self.number:
            clean_number = str(self.number).replace("+", "").replace(" ", "")
            return f"https://wa.me/{clean_number}"
        return ""

    # ------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return the formatted phone number."""
        return str(self.international_format)


# ==============================================
# Email Address model
# ==============================================
class Email(Address):
    """Stores email contact addresses with optional primary designation."""

    class Meta(Address.Meta):
        """Meta configuration."""

        ordering = ["display_order", "email"]

    # ------------------------------------------------------------------------

    email = models.EmailField(
        help_text="Email address for public contact or form submissions (e.g., user@example.com).",
        unique=True,
    )

    @property
    def mailto_link(self) -> str:
        """Return a mailto: link for use in templates and contact actions."""
        return f"mailto:{self.email}"

    # ------------------------------------------------------------------------

    def __str__(self) -> str:  # noqa: D105
        return str(self.email)


class PhysicalLocation(Address):
    """Stores physical location details with optional map and contact-form usage."""

    class Meta(Address.Meta):
        """Meta configuration."""

        ordering = ["display_order", "label", "city"]

    # ------------------------------------------------------------------------

    label = models.CharField(
        max_length=100,
        help_text="Short label for this location (e.g., Main Office).",
        unique=True,
    )

    # ------------------------------------------------------------------------

    building = models.CharField(
        max_length=100,
        blank=True,
        help_text="Building name, suite, or block (e.g., Britam Tower, Block A).",
    )

    # ------------------------------------------------------------------------

    street_address = models.CharField(
        max_length=255,
        help_text="Street line including number and street name.",
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        help_text="City, town, or locality.",
        blank=True,
    )

    state_province = models.CharField(
        max_length=100,
        blank=True,
        help_text="State, province, county, or region.",
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="ZIP or postal code.",
    )

    country = models.CharField(
        max_length=100,
        default="Kenya",
        help_text="Country name (defaults to Kenya).",
        blank=True,
    )

    @property
    def full_address(self) -> str:
        """Return a full address string assembled from available fields."""
        parts = [str(self.street_address), str(self.city)]
        if self.state_province:
            parts.append(str(self.state_province))
        if self.postal_code:
            parts.append(str(self.postal_code))
        parts.append(str(self.country))
        return ", ".join(parts)

    @property
    def short_address(self) -> str:
        """Return a short location string in city and country format."""
        return f"{self.city}, {self.country}"

    # ------------------------------------------------------------------------

    map_embed_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Embeddable map URL (for example, a Google Maps iframe source URL).",
    )

    # ------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return the label when available, otherwise fall back to city."""
        return str(self.label if self.label else self.city)
