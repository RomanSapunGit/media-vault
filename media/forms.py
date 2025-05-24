from django import forms


class GenreSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search name...',
            'type': 'text',
        }),
    )
