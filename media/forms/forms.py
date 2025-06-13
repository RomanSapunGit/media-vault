from django import forms

from media.forms.mixins import MediaFormMixin
from media.models import Genre, Book, Film


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


class BookForm(MediaFormMixin):
    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "created_at",
            "creators",
            "genres",
            "chapters",
            "type"
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "created_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "chapters": forms.NumberInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
        }


class FilmForm(MediaFormMixin):
    class Meta:
        model = Film
        fields = [
            "title",
            "description",
            "created_at",
            "creators",
            "genres",
            "country",
            "duration"
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "created_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "duration": forms.TimeInput(attrs={"class": "form-control"}),
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


class MediaUserUpdateForm(SetPasswordForm, forms.ModelForm):
    username = forms.CharField(
        label="Username",
        error_messages={"invalid": "Please enter a valid username."},
        widget=forms.TextInput(attrs={
            "class": "form-control",
        }
        )
    )

    new_password1 = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "form-control",
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirm password",
        required=True,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "form-control",
        }),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = MediaUser
        fields = ["username", "new_password1", "new_password2"]
