from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm

from media.forms.mixins import CustomErrorMessageMixin
from media.models import MediaUser


class MediaUserUpdateForm(
    SetPasswordForm,
    CustomErrorMessageMixin,
    forms.ModelForm
):
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
