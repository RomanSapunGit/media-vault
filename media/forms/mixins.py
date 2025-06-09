from django import forms

from media.models import Creator, Genre, Media


class MediaFormMixin(forms.ModelForm):
    creators = forms.ModelMultipleChoiceField(
        queryset=Creator.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )