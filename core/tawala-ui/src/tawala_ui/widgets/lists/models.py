"""Widget lists models."""

from django.db import models

from ...utils.models import (
    BootstrapIconModel,
    CreatedAtUpdatedAtModel,
    DisplayOrderModel,
    IsActiveIsPrimaryModel,
)


class Group(
    CreatedAtUpdatedAtModel,
    BootstrapIconModel,
    IsActiveIsPrimaryModel,
):
    """Model representing a list group."""

    class Meta(
        DisplayOrderModel.Meta,
        BootstrapIconModel.Meta,
        CreatedAtUpdatedAtModel.Meta,
        IsActiveIsPrimaryModel.Meta,
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
    DisplayOrderModel,
    BootstrapIconModel,
    CreatedAtUpdatedAtModel,
    IsActiveIsPrimaryModel,
):
    """Model representing an individual item within a list group."""

    class Meta(
        DisplayOrderModel.Meta,
        BootstrapIconModel.Meta,
        CreatedAtUpdatedAtModel.Meta,
        IsActiveIsPrimaryModel.Meta,
    ):
        """Meta configuration."""

        ordering = ["display_order", "name"]

    # ------------------------------------------------------------------------

    groups = models.ManyToManyField(
        Group,
        related_name="items",
        blank=True,
        help_text="Groups this item belongs to.",
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
