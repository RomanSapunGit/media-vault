from django import forms

from media.forms.mixins import CustomErrorMessageMixin
from media.models import (
    Creator, StatusChoices, Media,
    UserMediaRating
)


class CreatorForm(CustomErrorMessageMixin, forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
        }
        )
    )
    middle_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
        }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
        }
        )
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control", "type": "date"
        }
        )
    )

    class Meta:
        model = Creator
        fields = "__all__"


class MediaUserRatingForm(CustomErrorMessageMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.rating_id = kwargs.pop("id", "")
        super().__init__(*args, **kwargs)

    rating = forms.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=0.0,
        max_value=10.0,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "0.0",
            "max": "10.0",
            "step": "0.1"
        })
    )

    review = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5
        })
    )

    status = forms.ChoiceField(
        choices=StatusChoices.choices,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    is_hidden = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )

    media = forms.ModelChoiceField(
        queryset=Media.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        media = cleaned_data.get("media")
        if UserMediaRating.objects.filter(
                user=self.user,
                media=media
        ).exists() and not self.rating_id:

            msg = ("You already have a review/created the media."
                   " Please update it instead of creating new one or "
                   "choose another media for review")

            self.add_error("media", msg)

    class Meta:
        model = UserMediaRating
        fields = ["media", "rating", "review", "status", "is_hidden"]
