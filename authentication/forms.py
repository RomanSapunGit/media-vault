from django import forms
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       UsernameField)

from media.models import MediaUser


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Same password",
                "class": "form-control"
            }
        ))

    class Meta:
        model = MediaUser
        fields = ('username', 'email', 'password1', 'password2')


class MediaUserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "placeholder": "Username",
        "class": "form-control"
    }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "placeholder": "Password",
            "class": "form-control"
        }),
    )

    class Meta:
        model = MediaUser
        fields = ('username', 'password')
