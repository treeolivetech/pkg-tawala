# noqa: D100
from django import forms


class SearchForm(forms.Form):  # noqa: D101
    text = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={}),
    )
