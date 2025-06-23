from django import forms

from media.models import Creator, Genre


class MediaFormMixin(forms.ModelForm):
    BASE_FIELDS = (
        "title",
        "description",
        "created_at",
        "creators",
        "genres",
    )

    BASE_WIDGETS = {
        "title": forms.TextInput(attrs={"class": "form-control"}),
        "description": forms.Textarea(attrs={"class": "form-control"}),
        "created_at": forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        )
    }

    creators = forms.ModelMultipleChoiceField(
        queryset=Creator.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )


class CustomErrorMessageMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            label = (field.label or name
                     .replace('_', ' ')
                     .capitalize()
                     )
            field.error_messages = {
                'required':
                    f'The field {label} is required'
            }
