"""Widget Brand Models."""

from typing import Any, cast

from django.apps import AppConfig
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.templatetags.static import static

from ...utils.models import (
    CreatedAtUpdatedAtModel,
    DisplayOrderModel,
    ImageModel,
    IsActiveIsPrimaryModel,
)
from .apps import BrandConfig


# ==============================================
# Name
# ==============================================
# choices
class NameChoice(models.TextChoices):
    """Enums for brand name."""

    FULL_NAME = "full_name", "Full Name"
    SHORT_NAME = "short_name", "Short Name"
    LEGAL_NAME = "legal_name", "Legal Name"


# models
class Name(
    CreatedAtUpdatedAtModel,
    DisplayOrderModel,
):
    """Stores the name of the brand."""

    class Meta(DisplayOrderModel.Meta, CreatedAtUpdatedAtModel.Meta):
        """Meta configuration."""

        ordering = ["display_order", "type"]

    # ------------------------------------------------------------------------

    type = models.CharField(
        max_length=20,
        choices=NameChoice.choices,
        unique=True,
        help_text="Select the name type. Each type can only be added once.",
    )

    @property
    def display_type(self) -> str:
        """Return the human-friendly brand name from model choices."""
        return str(self.get_type_display())  # type: ignore

    # ------------------------------------------------------------------------

    value = models.CharField(
        max_length=255,
        blank=True,
        help_text="Enter the brand name of your organization/business/company.",
    )

    @property
    def data(self) -> str:
        """Return the brand name value."""
        if self.value:
            return str(self.value)
        match self.type:
            case NameChoice.FULL_NAME:
                return "Your Full Brand Name"
            case NameChoice.SHORT_NAME:
                return "Your Short Brand Name"
            case NameChoice.LEGAL_NAME:
                return "Your Legal Brand Name"
            case _:
                return "Unknown Brand Name"

    # ------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of the Name instance."""
        return f"{self.display_type} - {self.value}"


# signals
@receiver(post_migrate)
def create_default_names(sender: object, app_config: AppConfig, **kwargs: Any) -> None:
    """Seed one Name record per NameChoice on migration."""
    if app_config.name != BrandConfig.name:
        return
    for choice in NameChoice.values:
        cast(Any, Name).objects.get_or_create(type=choice)


# ==============================================
# Description
# ==============================================
# choices
class DescriptionChoice(models.TextChoices):
    """Enums for brand description."""

    SHORT = "short", "Short Description"
    LONG = "long", "Long Description"
    MISSION_STATEMENT = "mission_statement", "Mission Statement"
    VISION_STATEMENT = "vision_statement", "Vision Statement"


# models
class Description(
    CreatedAtUpdatedAtModel,
    DisplayOrderModel,
):
    """Stores a description of the brand."""

    class Meta(DisplayOrderModel.Meta, CreatedAtUpdatedAtModel.Meta):
        """Meta configuration."""

        ordering = ["display_order", "type"]

    # ------------------------------------------------------------------------

    type = models.CharField(
        max_length=20,
        choices=DescriptionChoice.choices,
        unique=True,
        help_text="Select the description type. Each type can only be added once.",
    )

    @property
    def display_type(self) -> str:
        """Return the human-friendly description type from model choices."""
        return str(self.get_type_display())  # type: ignore

    # ------------------------------------------------------------------------

    value = models.TextField(
        blank=True,
        help_text="Enter the description for your organization/business/company.",
    )

    @property
    def data(self) -> str:
        """Return the description value."""
        if self.value:
            return str(self.value)
        match self.type:
            case DescriptionChoice.SHORT:
                return "Your Short Description"
            case DescriptionChoice.LONG:
                return "Your Long Description"
            case DescriptionChoice.MISSION_STATEMENT:
                return "Your Mission Statement"
            case DescriptionChoice.VISION_STATEMENT:
                return "Your Vision Statement"
            case _:
                return "Unknown Description"

    # ------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of the Description instance."""
        return f"{self.display_type} - {str(self.value)[:50]}"


# signals
@receiver(post_migrate)
def create_default_descriptions(
    sender: object, app_config: AppConfig, **kwargs: Any
) -> None:
    """Seed one Description record per DescriptionChoice on migration."""
    if app_config.name != BrandConfig.name:
        return
    for choice in DescriptionChoice.values:
        cast(Any, Description).objects.get_or_create(type=choice)


# ==============================================
# Icon
# ==============================================
# choices
class IconChoice(models.TextChoices):
    """Choices for brand icon types."""

    FAVICON_ICO = "favicon_ico", "Favicon (.ico)"
    FAVICON_SVG = "favicon_svg", "Favicon (.svg)"
    APPLE_TOUCH_ICON = "apple_touch_icon", "Apple Touch Icon"


# models
class Icon(
    CreatedAtUpdatedAtModel,
    DisplayOrderModel,
    ImageModel,
):
    """Stores a brand icon image (e.g. favicon, Apple Touch Icon) per type."""

    class Meta(
        DisplayOrderModel.Meta,
        ImageModel.Meta,
        CreatedAtUpdatedAtModel.Meta,
    ):
        """Meta configuration."""

        ordering = ["display_order", "name"]

    # ------------------------------------------------------------------------

    name = models.CharField(
        max_length=20,
        choices=IconChoice.choices,
        unique=True,
        help_text="Select the icon type. Each type can only be added once.",
    )

    @property
    def display_name(self) -> str:
        """Return the human-friendly icon type name from model choices."""
        return str(self.get_name_display())  # type: ignore

    # ------------------------------------------------------------------------

    @property
    def data(self) -> str:
        """Return the URL of the image if it exists."""
        if self.image and hasattr(self.image, "url"):
            return str(self.image.url)

        match self.name:
            case IconChoice.FAVICON_ICO:
                return static("brand/favicon.ico")
            case IconChoice.FAVICON_SVG:
                return static("brand/favicon.svg")
            case IconChoice.APPLE_TOUCH_ICON:
                return static("brand/apple-touch-icon.png")
            case _:
                return ""

    # ------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of the Icon instance."""
        return str(self.display_name)


# signals
@receiver(post_migrate)
def create_default_icons(sender: object, app_config: AppConfig, **kwargs: Any) -> None:
    """Seed one Icon record per IconChoice on migration."""
    if app_config.name != BrandConfig.name:
        return
    for choice in IconChoice.values:
        cast(Any, Icon).objects.get_or_create(name=choice)


# ==============================================
# Logo
# ==============================================
# choices
class LogoVariantChoice(models.TextChoices):
    """Django-compatible choices for brand logo background variants."""

    LIGHT = "light", "Light Background"
    DARK = "dark", "Dark Background"
    COLORLESS = "colorless", "Colorless Background"


# models
class Logo(
    CreatedAtUpdatedAtModel,
    IsActiveIsPrimaryModel,
    DisplayOrderModel,
    ImageModel,
):
    """Stores a brand logo image per background variant (light, dark, colorless)."""

    class Meta(
        DisplayOrderModel.Meta,
        ImageModel.Meta,
        CreatedAtUpdatedAtModel.Meta,
        IsActiveIsPrimaryModel.Meta,
    ):
        """Meta configuration."""

        ordering = ["display_order", "name"]

    # ------------------------------------------------------------------------

    name = models.CharField(
        max_length=20,
        choices=LogoVariantChoice.choices,
        unique=True,
        help_text="Select the background variant this logo is optimised for. Each variant can only be added once.",
    )

    @property
    def display_name(self) -> str:
        """Return the human-friendly logo variant name from model choices."""
        return str(self.get_name_display())  # type: ignore

    # ------------------------------------------------------------------------

    @property
    def data(self) -> str:
        """Return the URL of the image if it exists."""
        if self.image and hasattr(self.image, "url"):
            return str(self.image.url)

        match self.name:
            case LogoVariantChoice.LIGHT:
                return static("brand/logo-light.png")
            case LogoVariantChoice.DARK:
                return static("brand/logo-dark.png")
            case LogoVariantChoice.COLORLESS:
                return static("brand/logo-colorless.png")
            case _:
                return ""

    # ------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of the Logo instance."""
        return str(self.display_name)


# signals
@receiver(post_migrate)
def create_default_logos(sender: object, app_config: AppConfig, **kwargs: Any) -> None:
    """Seed one Logo record per LogoVariantChoice on migration."""
    if app_config.name != BrandConfig.name:
        return
    for choice in LogoVariantChoice.values:
        cast(Any, Logo).objects.get_or_create(name=choice)
