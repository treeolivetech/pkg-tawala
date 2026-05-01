"""model utils."""

from typing import Any, cast

from django.db import models


class DisplayOrderModel(models.Model):
    """Abstract model providing a display order field."""

    class Meta:
        """Meta configuration."""

        abstract = True

    # ------------------------------------------------------------------------

    DISPLAY_ORDER_DEFAULT = 1
    DISPLAY_ORDER_HELP_TEXT = (
        "Display order (lower numbers - zero included - appear first)."
    )

    display_order = models.PositiveIntegerField(
        default=DISPLAY_ORDER_DEFAULT,
        help_text=DISPLAY_ORDER_HELP_TEXT,
    )


class BootstrapIconModel(models.Model):
    """Abstract model providing a Bootstrap icon field."""

    class Meta:
        """Meta configuration."""

        abstract = True

    BOOTSTRAP_ICON_HELP_TEXT = (
        "Optional Bootstrap icon class. Example: 'bi bi-cart' for a shopping cart icon. "
        "Find icons at [Bootstrap Icons](https://icons.getbootstrap.com/)."
    )

    bootstrap_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text=BOOTSTRAP_ICON_HELP_TEXT,
    )


class CreatedAtUpdatedAtModel(models.Model):
    """Abstract model providing created and updated timestamps."""

    class Meta:
        """Meta configuration."""

        abstract = True

    # ------------------------------------------------------------------------

    CREATED_AT_AUTO_NOW_ADD = True
    CREATED_AT_HELP_TEXT = "Date and time created."

    created_at = models.DateTimeField(
        auto_now_add=CREATED_AT_AUTO_NOW_ADD,
        help_text=CREATED_AT_HELP_TEXT,
    )

    # ------------------------------------------------------------------------

    UPDATED_AT_AUTO_NOW = True
    UPDATED_AT_HELP_TEXT = "Date and time last updated."

    updated_at = models.DateTimeField(
        auto_now=UPDATED_AT_AUTO_NOW,
        help_text=UPDATED_AT_HELP_TEXT,
    )


class ImageModel(models.Model):
    """Abstract model providing image utility fields and methods."""

    class Meta:
        """Meta configuration."""

        abstract = True

    IMAGE_UPLOAD_PATH = "base/images/"
    IMAGE_HELP_TEXT = "Upload an image file."

    image = models.ImageField(
        upload_to=IMAGE_UPLOAD_PATH,
        blank=True,
        null=True,
        help_text=IMAGE_HELP_TEXT,
    )

    # ------------------------------------------------------------------------

    IMAGE_ALT_HELP_TEXT = "Alternative text for accessibility."

    image_alt = models.CharField(
        max_length=255, blank=True, help_text=IMAGE_ALT_HELP_TEXT
    )


class IsActiveIsPrimaryModel(models.Model):
    """Abstract model providing an is_active and is_primary field."""

    class Meta:
        """Meta configuration."""

        abstract = True

    IS_ACTIVE_DEFAULT = True
    IS_ACTIVE_HELP_TEXT = "Designates whether this item should be treated as active. Unselect this instead of deleting items."

    is_active = models.BooleanField(
        default=IS_ACTIVE_DEFAULT,
        help_text=IS_ACTIVE_HELP_TEXT,
    )

    # ------------------------------------------------------------------------

    IS_PRIMARY_DEFAULT = False
    IS_PRIMARY_HELP_TEXT = (
        "Designates whether this item is the primary or default item. "
        "Only one active item should be marked as primary."
    )

    is_primary = models.BooleanField(
        default=IS_PRIMARY_DEFAULT,
        help_text=IS_PRIMARY_HELP_TEXT,
    )

    # ------------------------------------------------------------------------

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Enforce uniqueness of primary flag and inactive behavior.

        - Keep only one primary item.
        - Clear the primary flag when the record is inactive.
        """
        if not self.is_active:
            cast(Any, self).is_primary = False

        if self.is_primary:
            cast(Any, self.__class__).objects.filter(is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)

        super().save(*args, **kwargs)
