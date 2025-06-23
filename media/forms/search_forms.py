from django import forms


class GenreSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search name...",
                "type": "text",
            }
        ),
    )


class CreatorSearchForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by first name...",
                "type": "text",
            }
        ),
    )


class MediaSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search title...",
                "type": "text",
            }
        ),
    )
