from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from media.forms.search_forms import RatingSearchForm
from media.models import UserMediaRating
from media.views.mixins.media_mixin import MediaTypeFilterMixin, MediaNameSessionMixin
from media.views.mixins.mixins import (
    SearchMixin,

)
from media.views.mixins.rating_mixins import RatingViewMixin


class RatingListView(
    LoginRequiredMixin, MediaNameSessionMixin,
    SearchMixin, MediaTypeFilterMixin,
    generic.ListView
):
    model = UserMediaRating
    queryset = (UserMediaRating
                .objects
                .filter(is_hidden=False)
                .prefetch_related("user", "media")
                )
    paginate_by = 10
    search_form = RatingSearchForm
    template_name = "media/list/rating_list.html"
    context_object_name = "rating_list"


class RatingDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserMediaRating
    template_name = "media/detail/rating_detail.html"
    context_object_name = "rating"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = "rating"
        context["delete_url"] = reverse_lazy(
            "media:rating_delete",
            args=[context["rating"].id]
        )
        return context


class RatingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UserMediaRating

    def get_success_url(self):
        success_url = self.request.POST.get(
            "next",
            reverse_lazy("media:rating_list")
        )
        return success_url


class RatingCreateView(
    LoginRequiredMixin,
    RatingViewMixin,
    generic.CreateView
):
    success_url = reverse_lazy("media:rating_list")


class RatingUpdateView(
    LoginRequiredMixin,
    RatingViewMixin,
    generic.UpdateView
):
    def get_success_url(self):
        if "next" in self.request.GET:
            success_url = reverse_lazy(
                "media:user_detail",
                args=[self.request.GET.get("user_id", "1")]
            )
        else:
            success_url = reverse_lazy(
                "media:rating_detail",
                args=[self.kwargs["pk"]]
            )
        return success_url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"id": self.kwargs["pk"]})
        return kwargs
