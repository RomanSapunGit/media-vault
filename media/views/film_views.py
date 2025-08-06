from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from media.forms.search_forms import MediaSearchForm
from media.models import Film
from media.views.mixins.media_mixin import MediaListMixin, FilmMutateMixin
from media.views.mixins.mixins import SearchMixin


class FilmListView(
    LoginRequiredMixin,
    MediaListMixin,
    SearchMixin,
    generic.ListView
):
    model = Film
    paginate_by = 10
    template_name = "media/list/film_list.html"
    search_form = MediaSearchForm
    url_create = reverse_lazy("media:film_create")


class FilmDetailView(LoginRequiredMixin, generic.DetailView):
    model = Film
    template_name = "media/detail/film_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = "film"
        context["delete_url"] = reverse_lazy(
            "media:film_delete",
            args=[context["film"].id]
        )
        return context


class FilmCreateView(LoginRequiredMixin, FilmMutateMixin, generic.CreateView):
    success_url = reverse_lazy("media:film_list")


class FilmUpdateView(LoginRequiredMixin, FilmMutateMixin, generic.UpdateView):
    def get_success_url(self):
        return reverse_lazy("media:film_detail", kwargs={"pk": self.object.id})


class FilmDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Film
    success_url = reverse_lazy("media:film_list")
