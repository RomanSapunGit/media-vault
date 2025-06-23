from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from media.forms.search_forms import MediaSearchForm
from media.models import Series
from media.utils import get_reverse_choice
from media.views.mixins.media_mixin import MediaListMixin, SeriesMutateMixin
from media.views.mixins.mixins import (
    SearchMixin,
    TypeChoiceMixin
)


class SeriesListView(
    LoginRequiredMixin,
    MediaListMixin,
    SearchMixin,
    TypeChoiceMixin,
    generic.ListView
):
    model = Series
    paginate_by = 10
    template_name = "media/list/series_list.html"
    search_form = MediaSearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["status_choices"] = [
            choice_status[1]
            for choice_status in Series.status.field.choices
        ]
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        status_choice = self.request.GET.get("status")
        db_stored_choice = get_reverse_choice(status_choice, Series.status)
        if db_stored_choice:
            queryset = queryset.filter(
                status=db_stored_choice
            )
        return queryset


class SeriesCreateView(
    LoginRequiredMixin, SeriesMutateMixin,
    generic.CreateView
):
    success_url = reverse_lazy("media:series_list")


class SeriesUpdateView(
    LoginRequiredMixin, SeriesMutateMixin,
    generic.UpdateView
):
    def get_success_url(self):
        return reverse_lazy(
            "media:series_detail", kwargs={"pk": self.object.id}
        )


class SeriesDetailView(LoginRequiredMixin, generic.DetailView):
    model = Series
    template_name = "media/detail/series_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = "series"
        context["delete_url"] = reverse_lazy(
            "media:series_delete",
            args=[context["series"].id]
        )
        return context


class SeriesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Series
    success_url = reverse_lazy("media:series_list")
