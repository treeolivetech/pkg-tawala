"""Widget addresses forms."""

from django import forms
from tawala_api.utils.forms import UniqueChoiceFormMixin

from .models import Social


class SocialMediaAddressForm(UniqueChoiceFormMixin, forms.ModelForm):
    """Form for SocialMediaAddress model, filtering out existing choices for 'name'.

    Excludes the 'icon' field from the form.
    """

    class Meta:
        """Meta options for the form."""

        model = Social
        fields = "__all__"
        exclude = ("icon",)


# class EmailUsForm(forms.Form):
#     name = forms.CharField(
#         label="Your Name",
#         max_length=100,
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
#     )
#     email = forms.EmailField(
#         label="Your Email",
#         widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
#     )
#     subject = forms.CharField(
#         label="Subject",
#         max_length=200,
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
#     )
#     message = forms.CharField(
#         label="Message",
#         widget=forms.Textarea(
#             attrs={"class": "form-control", "rows": "5", "placeholder": "Message"}
#         ),
#     )

#     def clean_message(self):
#         message = self.cleaned_data.get("message", "")
#         if len(message.strip()) < 10:
#             raise forms.ValidationError("Message must be at least 10 characters long.")
#         return message
