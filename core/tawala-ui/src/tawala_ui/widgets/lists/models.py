"""Widget lists models."""

from django.db import models
from tawala_api.utils.models import (
    AbstractBootstrapIcon,
    AbstractCreatedAtUpdatedAt,
    AbstractDisplayOrder,
    AbstractIsActiveIsPrimary,
)


class Group(
    AbstractCreatedAtUpdatedAt, AbstractBootstrapIcon, AbstractIsActiveIsPrimary
):
    """Model representing a list group."""

    class Meta(
        AbstractCreatedAtUpdatedAt.Meta,
        AbstractBootstrapIcon.Meta,
        AbstractIsActiveIsPrimary.Meta,
    ):
        """Meta configuration."""

        ordering = ["name"]

    # ------------------------------------------------------------------------

    name = models.CharField(
        max_length=255,
        help_text="Group name that groups related list items (e.g., 'Electronics', 'Furniture').",
    )

    # ------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of the Group."""
        return str(self.name)


class Item(
    AbstractDisplayOrder,
    AbstractBootstrapIcon,
    AbstractCreatedAtUpdatedAt,
    AbstractIsActiveIsPrimary,
):
    """Model representing an individual item within a list group."""

    class Meta(
        AbstractDisplayOrder.Meta,
        AbstractBootstrapIcon.Meta,
        AbstractCreatedAtUpdatedAt.Meta,
        AbstractIsActiveIsPrimary.Meta,
    ):
        """Meta configuration."""

        ordering = ["display_order", "name"]

    # ------------------------------------------------------------------------

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="items",
    )

    # ------------------------------------------------------------------------

    name = models.CharField(
        max_length=255,
        help_text="Name of the item.",
    )

    # ------------------------------------------------------------------------

    description = models.TextField(
        blank=True,
        help_text="Detailed description of this item, including features or specifications (optional).",
    )

    # ------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of the ListItem."""
        return str(self.name)
