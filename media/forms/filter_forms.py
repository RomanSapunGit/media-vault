from django import forms

from media.models import Genre, Creator


class GenreFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["genres"].choices = [
            (genre.name, genre.name) for genre in Genre.objects.all()
        ]

    genres = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "d-flex flex-wrap gap-2"
            }
        ),
    )


class CreatorFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["creators"].choices = [
            (creator.first_name, creator.first_name)
            for creator in Creator.objects.all()
        ]
    creators = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "d-flex flex-wrap gap-2"
            }
        ),
    )
