"""Widget lists admin configuration."""

from typing import Any, cast

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Group, Item


@admin.register(Group)
class ListGroupAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    """List Group Admin. Allow permissions only for superusers."""

    list_display = ("name", "is_primary", "is_active")
    list_filter = ("is_active", "is_primary")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")

    def get_fieldsets(
        self, request: HttpRequest, obj: Group | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets including timestamps on edit."""
        return [
            ("Group Details", {"fields": ("name",)}),
            (
                "Display Options",
                {
                    "fields": (
                        "bootstrap_icon",
                        "is_primary",
                        "is_active",
                    )
                },
            ),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]


class GroupNameFilter(admin.SimpleListFilter):
    """Custom filter for Item based on group name."""

    title = "Group"
    parameter_name = "group_name"

    def lookups(self, request: HttpRequest, model_admin: Any) -> list[tuple[str, str]]:
        """Return a list of tuples for the filter choices."""
        groups = set(cast(Any, Group).objects.values_list("name", flat=True))
        return [(str(name), str(name)) for name in groups]

    def queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> QuerySet[Any]:
        """Filter the queryset based on the selected group name."""
        if self.value():
            return cast(Any, queryset.filter(groups__name=self.value()))
        return queryset


@admin.register(Item)
class ListItemAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    """List Item Admin with enhanced display, filtering, search, and form behavior."""

    list_display = (
        "name",
        "bootstrap_icon",
        "get_groups",
        "is_primary",
        "is_active",
        "display_order",
    )
    list_editable = (
        "bootstrap_icon",
        "display_order",
    )
    list_filter = (GroupNameFilter, "groups", "is_active", "is_primary")
    search_fields = ("name", "description")
    ordering = ("display_order", "name")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("groups",)  # ← the two-box widget with arrows

    @admin.display(description="Groups")
    def get_groups(self, obj: Item) -> str:
        """Return a comma-separated list of group names."""
        return ", ".join(obj.groups.values_list("name", flat=True))  # type: ignore

    def get_fieldsets(
        self, request: HttpRequest, obj: Item | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets including timestamps on edit."""
        return [
            ("Item Details", {"fields": ("name", "description", "groups")}),
            (
                "Display Options",
                {
                    "fields": (
                        "bootstrap_icon",
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
