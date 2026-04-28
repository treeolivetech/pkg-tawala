"""Widget addresses forms."""

from django import forms
from tawala_api.utils.forms import UniqueChoiceFormMixin

from .models import Social


class SocialMediaAddressForm(UniqueChoiceFormMixin, forms.ModelForm):
    """Form for the Social model, filtering out existing choices for 'name'.

    Excludes the auto-populated 'icon' field from the form.
    """

    class Meta:
        """Meta options for the form."""

        model = Social
        fields = "__all__"
        exclude = ("icon",)
