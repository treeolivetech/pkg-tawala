"""Widget lists models."""

from django.db import models

from treeolive_api.contrib.ui.models import (
    AbstractBootstrapIcon,
    AbstractCreatedAtUpdatedAt,
    AbstractDisplayOrder,
)


class Category(AbstractCreatedAtUpdatedAt):
    """Model representing a category that groups related list items."""

    class Meta(AbstractCreatedAtUpdatedAt.Meta):
        """Meta configuration."""

        ordering = ["name"]
        verbose_name_plural = "List categories"

    name = models.CharField(
        max_length=255,
        help_text="Category name that groups related list items (e.g., 'Electronics', 'Furniture').",
    )

    def __str__(self) -> str:
        """Return a string representation of the ListCategory."""
        return str(self.name)


class Item(AbstractDisplayOrder, AbstractBootstrapIcon, AbstractCreatedAtUpdatedAt):
    """Model representing an individual item within a list widget."""

    class Meta(
        AbstractDisplayOrder.Meta,
        AbstractBootstrapIcon.Meta,
        AbstractCreatedAtUpdatedAt.Meta,
    ):
        """Meta configuration."""

        ordering = ["display_order", "name"]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the item.",
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of this item, including features or specifications (optional).",
    )

    def __str__(self) -> str:
        """Return a string representation of the ListItem."""
        return str(self.name)
