from django import forms

from media.forms.mixins import MediaFormMixin, CustomErrorMessageMixin
from media.models import Series, Book, Film


class BookForm(CustomErrorMessageMixin, MediaFormMixin):
    class Meta:
        model = Book
        fields = MediaFormMixin.BASE_FIELDS + (
            "chapters",
            "type"
        )
        widgets = {
            **MediaFormMixin.BASE_WIDGETS,
            "chapters": forms.NumberInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
        }


class FilmForm(CustomErrorMessageMixin, MediaFormMixin):
    class Meta:
        model = Film
        fields = MediaFormMixin.BASE_FIELDS + (
            "country",
            "duration"
        )
        widgets = {
            **MediaFormMixin.BASE_WIDGETS,
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "duration": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
        }


class SeriesForm(MediaFormMixin):
    class Meta:
        model = Series
        fields = MediaFormMixin.BASE_FIELDS + (
            "country",
            "status",
            "seasons",
            "series_number",
            "type"
        )

        widgets = {
            **MediaFormMixin.BASE_WIDGETS,
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "seasons": forms.NumberInput(attrs={"class": "form-control"}),
            "series_number": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "type": forms.Select(attrs={"class": "form-control"}),
        }
