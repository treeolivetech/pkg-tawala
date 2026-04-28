"""Widget Brand Admin."""

from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from ...utils.admin import UniqueChoiceForm
from .models import Description, Icon, Logo, Name


# ==============================================
# Name
# ==============================================
# forms
class NameForm(UniqueChoiceForm):
    """Form for the Name model, filtering out existing choices for 'name'."""

    choice_field_name = "type"

    class Meta:
        """Meta options for the form."""

        model = Name
        fields = "__all__"


# admin
@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    """Brand Name Admin."""

    form = NameForm
    list_display = ("type", "value", "display_order")
    list_editable = ("value", "display_order")
    search_fields = ("type", "value")
    readonly_fields = ("created_at", "updated_at")

    def get_exclude(
        self, request: HttpRequest, obj: Name | None = None
    ) -> tuple[str, ...]:
        """Exclude 'type' on edit so the name type cannot be changed after creation."""
        if obj:
            return ("type",)
        return ()

    def get_fieldsets(
        self, request: HttpRequest, obj: Name | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets; omit 'type' when editing an existing record."""
        return [
            (
                "Brand Name Details",
                {
                    "fields": ("value",) if obj else ("type", "value"),
                },
            ),
            ("Display Options", {"fields": ("display_order")}),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]


# ==============================================
# Description
# ==============================================
# forms
class DescriptionForm(UniqueChoiceForm):
    """Form for the Description model, filtering out existing choices for 'type'."""

    choice_field_name = "type"

    class Meta:
        """Meta options for the form."""

        model = Description
        fields = "__all__"


# admin
@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    """Brand Description Admin."""

    form = DescriptionForm
    list_display = ("type", "value", "display_order")
    list_editable = ("value", "display_order")
    search_fields = ("type", "value")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("type",)

    def get_exclude(
        self, request: HttpRequest, obj: Description | None = None
    ) -> tuple[str, ...]:
        """Exclude 'type' on edit so the description type cannot be changed after creation."""
        if obj:
            return ("type",)
        return ()

    def get_fieldsets(
        self, request: HttpRequest, obj: Description | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets; omit 'type' when editing an existing record."""
        return [
            (
                "Brand Description Details",
                {
                    "fields": ("value",) if obj else ("type", "value"),
                },
            ),
            ("Display Options", {"fields": ("display_order",)}),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]


# ==============================================
# Icon
# ==============================================
# forms
class IconForm(UniqueChoiceForm):
    """Form for the Icon model, filtering out existing choices for 'name'."""

    choice_field_name = "name"

    class Meta:
        """Meta options for the form."""

        model = Icon
        fields = "__all__"


# admin
@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    """Brand Icon Admin."""

    form = IconForm
    list_display = ("name", "image", "display_order")
    list_editable = ("display_order",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")

    def get_exclude(
        self, request: HttpRequest, obj: Icon | None = None
    ) -> tuple[str, ...]:
        """Exclude 'name' on edit so the icon type cannot be changed after creation."""
        if obj:
            return ("name",)
        return ()

    def get_fieldsets(
        self, request: HttpRequest, obj: Icon | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets."""
        return [
            (
                "Icon Details",
                {
                    "fields": ("image",) if obj else ("name", "image"),
                },
            ),
            ("Display Options", {"fields": ("display_order",)}),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]


# ==============================================
# Logo
# ==============================================
# forms
class LogoForm(UniqueChoiceForm):
    """Form for the Logo model, filtering out existing choices for 'name'."""

    choice_field_name = "name"

    class Meta:
        """Meta options for the form."""

        model = Logo
        fields = "__all__"


# admin
@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    """Brand Logo Admin."""

    form = LogoForm
    list_display = ("name", "image", "is_primary", "is_active", "display_order")
    list_editable = ("display_order",)
    list_filter = ("is_active", "is_primary")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")

    def get_exclude(
        self, request: HttpRequest, obj: Logo | None = None
    ) -> tuple[str, ...]:
        """Exclude 'name' on edit so the logo variant cannot be changed after creation."""
        if obj:
            return ("name",)
        return ()

    def get_fieldsets(
        self, request: HttpRequest, obj: Logo | None = None
    ) -> list[tuple[str | None, dict[str, Any]]]:
        """Define fieldsets."""
        return [
            (
                "Logo Details",
                {
                    "fields": ("image",) if obj else ("name", "image"),
                },
            ),
            (
                "Display Options",
                {"fields": ("is_primary", "is_active", "display_order")},
            ),
            *(
                [("Timestamps", {"fields": ("created_at", "updated_at")})]
                if obj
                else []
            ),
        ]
