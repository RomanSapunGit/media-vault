from media.forms.forms import MediaUserRatingForm
from media.models import UserMediaRating


class RatingViewMixin:
    model = UserMediaRating
    form_class = MediaUserRatingForm
    template_name = "media/form/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_name"] = "rating"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs
