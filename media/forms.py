from django import forms

from media.models import Media, Genre


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


class GenreFilterForm(forms.Form):
    genres = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "d-flex flex-wrap gap-2"
            }
        ),
        choices=[(genre.name, genre.name) for genre in Genre.objects.all()]
    )


class MediaMutateForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = "__all__"

    def clean_genres(self):
        genres = self.cleaned_data.get("genres")
        if not genres:
            raise forms.ValidationError("You must select at least one genre.")
        return genres
