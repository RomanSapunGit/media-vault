from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from media.forms.forms import CreatorForm
from media.forms.search_forms import GenreSearchForm, CreatorSearchForm
from media.models import Genre, Media, Creator, UserMediaRating
from media.views.mixins.media_mixin import (
    MediaNameSessionMixin,
    MediaTypeCountMixin
)
from media.views.mixins.mixins import (
    SearchMixin
)


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    media_users_count = get_user_model().objects.count()
    context = {
        "media_users_count": media_users_count,
        "media_titles_count": Media.objects.all().count(),
        "media_ratings_count": UserMediaRating.objects.all().count()
    }
    return render(request, "home/index.html", context)


class GenreListView(
    LoginRequiredMixin,
    SearchMixin,
    MediaNameSessionMixin,
    MediaTypeCountMixin,
    generic.ListView
):
    model = Genre
    template_name = "media/list/genre_list.html"
    paginate_by = 10
    search_form = GenreSearchForm


class CreatorListView(
    LoginRequiredMixin,
    MediaNameSessionMixin,
    SearchMixin,
    MediaTypeCountMixin,
    generic.ListView
):
    model = Creator
    template_name = "media/list/creator_list.html"
    paginate_by = 10
    search_form = CreatorSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = "creator"
        context["no_media_with_creator"] = any(
            creator.media_type_count
            for creator in context["creator_list"]
        )
        return context


class CreatorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Creator
    form_class = CreatorForm
    template_name = "media/form/form.html"
    success_url = reverse_lazy("media:creator_list")

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'author': {
                    'id': self.object.id,
                    'name': str(self.object),
                }
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(
                'media/form/modal/create_author_modal.html', {
                    'creator_form': form
                }, request=self.request)
            return JsonResponse({'success': False, 'form_html': html})
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_name"] = "creator"
        return context


class CreatorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Creator
    success_url = reverse_lazy("media:creator_list")


class CreatorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Creator
    form_class = CreatorForm
    template_name = "media/form/form.html"
    success_url = reverse_lazy("media:creator_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_name"] = "creator"
        return context
