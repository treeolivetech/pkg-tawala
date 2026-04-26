"""Core forms and form mixins."""

from typing import Any


class UniqueChoiceFormMixin:
    """Mixin that filters a choice field to values not yet used.

    By default it targets the `name` field, but forms can override
    `choice_field_name` when a different field should be filtered.
    """

    choice_field_name = "name"

    instance: Any
    _meta: Any
    fields: dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the form and dynamically filter available choice values.

        It limits the choices based on which ones are not already used in the database.
        """
        super().__init__(*args, **kwargs)

        field_name = self.choice_field_name

        if self.instance.pk or field_name not in self.fields:
            return

        model_choices = self._get_model_choices(field_name)
        if not model_choices:
            return

        existing_values = self._meta.model.objects.values_list(field_name, flat=True)

        available_choices = [
            choice for choice in model_choices if choice[0] not in existing_values
        ]

        self.fields[field_name].choices = [(None, "")] + available_choices

    def _get_model_choices(self, field_name: str) -> list[tuple[Any, Any]]:
        """Return model choices from the configured field."""
        field = self._meta.model._meta.get_field(field_name)
        return list(getattr(field, "choices", []) or [])
