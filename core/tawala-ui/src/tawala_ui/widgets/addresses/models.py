"""Widget Addresses Models."""

from typing import Any, cast

from django.apps import AppConfig
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from ...utils.models import (
    CreatedAtUpdatedAtModel,
    DisplayOrderModel,
    IsActiveIsPrimaryModel,
)
from .apps import AddressesConfig


# ==============================================
# Address
# ==============================================
# choices
class SocialPlatformChoice(models.TextChoices):
    """Django-compatible social media choices for model fields."""

    FACEBOOK = "facebook", "Facebook"
    TWITTER = "twitter", "X (formerly Twitter)"
    INSTAGRAM = "instagram", "Instagram"
    LINKEDIN = "linkedin", "LinkedIn"
    YOUTUBE = "youtube", "YouTube"
    TIKTOK = "tiktok", "TikTok"
    PINTEREST = "pinterest", "Pinterest"
    SNAPCHAT = "snapchat", "Snapchat"
    DISCORD = "discord", "Discord"
    TELEGRAM = "telegram", "Telegram"
    GITHUB = "github", "GitHub"
    REDDIT = "reddit", "Reddit"
    TWITCH = "twitch", "Twitch"

    @classmethod
    def icon_for_value(cls, value: str) -> str:
        """Return the Bootstrap icon CSS class for the given platform value."""
        match value:
            case cls.FACEBOOK:
                return "bi bi-facebook"
            case cls.TWITTER:
                return "bi bi-twitter-x"
            case cls.INSTAGRAM:
                return "bi bi-instagram"
            case cls.LINKEDIN:
                return "bi bi-linkedin"
            case cls.YOUTUBE:
                return "bi bi-youtube"
            case cls.TIKTOK:
                return "bi bi-tiktok"
            case cls.PINTEREST:
                return "bi bi-pinterest"
            case cls.SNAPCHAT:
                return "bi bi-snapchat"
            case cls.DISCORD:
                return "bi bi-discord"
            case cls.TELEGRAM:
                return "bi bi-telegram"
            case cls.GITHUB:
                return "bi bi-github"
            case cls.REDDIT:
                return "bi bi-reddit"
            case cls.TWITCH:
                return "bi bi-twitch"
            case _:
                return ""

    @classmethod
    def base_url_for_value(cls, value: str) -> str:
        """Return the base profile URL for the given platform value."""
        match value:
            case cls.FACEBOOK:
                return "https://www.facebook.com/"
            case cls.TWITTER:
                return "https://x.com/"
            case cls.INSTAGRAM:
                return "https://www.instagram.com/"
            case cls.LINKEDIN:
                return "https://www.linkedin.com/in/"
            case cls.YOUTUBE:
                return "https://www.youtube.com/"
            case cls.TIKTOK:
                return "https://www.tiktok.com/"
            case cls.PINTEREST:
                return "https://www.pinterest.com/"
            case cls.SNAPCHAT:
                return "https://www.snapchat.com/add/"
            case cls.DISCORD:
                return "https://discord.gg/"
            case cls.TELEGRAM:
                return "https://t.me/"
            case cls.GITHUB:
                return "https://github.com/"
            case cls.REDDIT:
                return "https://www.reddit.com/user/"
            case cls.TWITCH:
                return "https://www.twitch.tv/"
            case _:
                return ""

    @classmethod
    def uses_at_prefix_for_value(cls, value: str) -> bool:
        """Return True if the platform requires a leading '@' in its username."""
        return value in {cls.YOUTUBE, cls.TIKTOK}

    @classmethod
    def build_profile_url_for_value(cls, value: str, username: str) -> str:
        """Return the full profile URL for the given platform and username."""
        base = cls.base_url_for_value(value)
        if not base:
            return ""
        uses_at = cls.uses_at_prefix_for_value(value)
        clean = username.lstrip("@")
        return f"{base}{'@' if uses_at else ''}{clean}"


# models
class Address(
    CreatedAtUpdatedAtModel,
    IsActiveIsPrimaryModel,
    DisplayOrderModel,
):
    """Shared base for all address records."""

    class Meta(
        CreatedAtUpdatedAtModel.Meta,
        IsActiveIsPrimaryModel.Meta,
        DisplayOrderModel.Meta,
    ):
        """Meta configuration."""

        abstract = True


# ==============================================
# Social
# ==============================================
class Social(Address):
    """Stores one social profile username per platform with an auto-generated icon and URL."""

    class Meta(Address.Meta):
        """Meta configuration."""

        ordering = ["display_order", "name"]

    # ------------------------------------------------------------------------

    name = models.CharField(
        max_length=20,
        choices=SocialPlatformChoice.choices,
        unique=True,
        help_text="Select the social platform. Each platform can only be added once.",
    )

    @property
    def display_name(self) -> str:
        """Return the human-friendly platform name from model choices."""
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
        blank=True,
        help_text=(
            "Your handle or username on this platform (e.g. 'johndoe' or 'acme-corp'). "
            "Do not include the full URL — it is built automatically from the platform. "
            "For YouTube and TikTok the '@' prefix is added automatically if omitted."
        ),
    )

    @property
    def url(self) -> str:
        """Return the full profile URL constructed from the platform base URL and username."""
        return SocialPlatformChoice.build_profile_url_for_value(
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
        if SocialPlatformChoice.uses_at_prefix_for_value(platform_value):
            if not username.startswith("@"):
                username = f"@{username}"
        else:
            username = username.lstrip("@")

        cast(Any, self).username = username
        cast(Any, self).icon = SocialPlatformChoice.icon_for_value(platform_value)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return a string representation of the Social address."""
        return f"{self.display_name} - {self.url}"


# signals
@receiver(post_migrate)
def create_default_socials(
    sender: object, app_config: AppConfig, **kwargs: Any
) -> None:
    """Seed one Social record per SocialPlatformChoice on migration."""
    if app_config.name != AddressesConfig.name:
        return
    for choice in SocialPlatformChoice.values:
        cast(Any, Social).objects.get_or_create(name=choice)


# ==============================================
# Phone
# ==============================================
# models
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
# Email
# ==============================================
# models
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


# ==============================================
# Physical Location
# ==============================================
# models
class PhysicalLocation(Address):
    """Stores physical location details with optional map and contact-form usage."""

    class Meta(Address.Meta):
        """Meta configuration."""

        ordering = ["display_order", "name", "city"]

    # ------------------------------------------------------------------------

    name = models.CharField(
        max_length=100,
        help_text="Name for this location (e.g., Main Office).",
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
        """Return the name when available, otherwise fall back to city."""
        return str(self.name if self.name else self.city)
