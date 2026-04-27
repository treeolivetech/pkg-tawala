"""Core model backends."""

from django.conf import settings
from django.db import models


class AbstractDisplayOrder(models.Model):
    """Abstract model providing a display order field."""

    class Meta:
        """Model metadata."""

        abstract = True

    display_order = models.PositiveIntegerField(
        default=1,
        help_text="Display order (lower numbers - zero included - appear first)",
    )


class AbstractBootstrapIcon(models.Model):
    """Abstract model providing a Bootstrap icon field."""

    class Meta:
        """Model metadata."""

        abstract = True

    bootstrap_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional Bootstrap icon class. Example: 'bi bi-cart' for a shopping cart icon. Find icons at [Bootstrap Icons](https://icons.getbootstrap.com/).",
    )


class AbstractCreatedAtUpdatedAt(models.Model):
    """Abstract model providing created and updated timestamps."""

    class Meta:
        """Model metadata."""

        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time last updated.",
    )


class AbstractImage(models.Model):
    """Abstract model providing image utility fields and methods."""

    class Meta:
        """Model metadata."""

        abstract = True

    image = models.ImageField(
        upload_to=f"{settings.CORE_APP}/images/",
        blank=True,
        null=True,
        help_text="Optional Image.",
    )
    image_alt_text = models.CharField(
        max_length=255, blank=True, help_text="Alternative text for accessibility."
    )

    @property
    def image_url(self) -> str:
        """Return the URL of the image if it exists."""
        if self.image and hasattr(self.image, "url"):
            return str(self.image.url)

        from django.templatetags.static import static

        return static(
            "core/placeholder.png"
        )  # TODO TEST: Use findstatic to find a default image in the static files.


class AbstractIsActive(models.Model):
    """Abstract model providing an is_active field."""

    class Meta:
        """Model metadata."""

        abstract = True

    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this item should be treated as active. Unselect this instead of deleting items.",
    )
