"""Widget addresses admin configuration."""

from typing import Any, cast

from django.contrib import admin
from django.http import HttpRequest

from .forms import SocialMediaAddressForm
from .models import (
    Email,
    Phone,
    PhysicalLocation,
    Social,
)


@admin.register(Social)
class SocialAddressAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    """Social Media Address Admin."""

    form = SocialMediaAddressForm
    list_display = ("name", "url", "is_active", "display_order")
    list_editable = ("url", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "url")
    readonly_fields = ("created_at", "updated_at")

    def get_exclude(
        self, request: HttpRequest, obj: Social | None = None
    ) -> tuple[str, ...]:
        """Exclude `name` on edit so platform cannot be changed after creation."""
        if obj:
            return ("name",)
        return ()

    def get_fieldsets(
        self, request: HttpRequest, obj: Social | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Remove `name` from edit fieldsets to match edit-time exclusions."""
        return [
            (
                "Social Media Details",
                {"fields": ("url",) if obj else ("name", "url")},
            ),
            ("Display Options", {"fields": ("is_active", "display_order")}),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]


@admin.register(Phone)
class PhoneAddressAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    """Phone Address Admin."""

    list_display = ("number", "is_primary", "is_active", "display_order")
    list_editable = ("display_order",)
    list_filter = ("is_active", "is_primary")
    search_fields = ("number",)
    readonly_fields = ("created_at", "updated_at", "current_primary_number")

    @admin.display(description="Current primary")
    def current_primary_number(self, obj: Phone | None) -> str:
        """Return the currently designated primary phone number."""
        primary = cast(Any, Phone).objects.filter(is_primary=True).first()
        return str(primary) if primary else "—"

    def get_exclude(
        self, request: HttpRequest, obj: Social | None = None
    ) -> tuple[str, ...]:
        """Exclude `number` on edit so platform cannot be changed after creation."""
        if obj:
            return ("number",)
        return ()

    def get_fieldsets(
        self, request: HttpRequest, obj: Phone | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets including timestamps."""
        return [
            *([("Phone Number Details", {"fields": ("number",)})] if not obj else []),
            (
                "Display Options",
                {
                    "fields": (
                        "current_primary_number",
                        "is_primary",
                        "is_active",
                        "display_order",
                    )
                },
            ),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]


@admin.register(Email)
class EmailAddressAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    """Email Address Admin."""

    list_display = ("email", "is_primary", "is_active", "display_order")
    list_editable = ("display_order",)
    list_filter = ("is_active", "is_primary")
    search_fields = ("email",)
    readonly_fields = ("created_at", "updated_at", "current_primary_email")

    @admin.display(description="Current primary")
    def current_primary_email(self, obj: Email | None) -> str:
        """Return the currently designated primary email address."""
        primary = cast(Any, Email).objects.filter(is_primary=True).first()
        return str(primary) if primary else "—"

    def get_exclude(
        self, request: HttpRequest, obj: Social | None = None
    ) -> tuple[str, ...]:
        """Exclude `email` on edit so platform cannot be changed after creation."""
        if obj:
            return ("email",)
        return ()

    def get_fieldsets(
        self, request: HttpRequest, obj: Email | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets including timestamps."""
        return [
            *([("Email Address Details", {"fields": ("email",)})] if not obj else []),
            (
                "Display Options",
                {
                    "fields": (
                        "current_primary_email",
                        "is_primary",
                        "is_active",
                        "display_order",
                    )
                },
            ),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]


@admin.register(PhysicalLocation)
class PhysicalAddressAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    """Physical Address Admin."""

    list_display = (
        "label",
        "city",
        "country",
        "is_primary",
        "is_active",
        "display_order",
    )
    list_editable = ("display_order",)
    list_filter = ("is_active", "is_primary", "country", "state_province")
    search_fields = ("label", "street_address", "city", "country")
    readonly_fields = ("created_at", "updated_at", "current_primary_location")

    @admin.display(description="Current primary")
    def current_primary_location(self, obj: PhysicalLocation | None) -> str:
        """Return the currently designated primary physical location."""
        primary = cast(Any, PhysicalLocation).objects.filter(is_primary=True).first()
        return str(primary) if primary else "—"

    def get_fieldsets(
        self, request: HttpRequest, obj: PhysicalLocation | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets including timestamps on edit."""
        return [
            (
                "Address Details",
                {
                    "fields": (
                        "label",
                        "building",
                        "street_address",
                        "city",
                        "state_province",
                        "postal_code",
                        "country",
                        "map_embed_url",
                    )
                },
            ),
            (
                "Display Options",
                {
                    "fields": (
                        "current_primary_location",
                        "is_primary",
                        "is_active",
                        "display_order",
                    )
                },
            ),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]
