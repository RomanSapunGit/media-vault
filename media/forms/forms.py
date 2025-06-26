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
