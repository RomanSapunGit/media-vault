from django import forms

from media.forms.mixins import CustomErrorMessageMixin
from media.models import (
    Creator, StatusChoices, Media,
    UserMediaRating
)



