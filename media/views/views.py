from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from media.forms.forms import (
    GenreSearchForm,
)
from media.models import Genre, Book, Film
from media.views.mixins import BookMutateMixin, FilmMutateMixin, MediaListMixin


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    media_users_count = get_user_model().objects.count()
    context = {
        "media_users_count": media_users_count
    }
    return render(request, "home/index.html", context)


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name = "media/genre-list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["search_form"] = GenreSearchForm(self.request.GET)

        media_dict = {
            "book": reverse("media:book_list"),
            "film": reverse("media:film_list"),
            "comic": reverse("media:comic_list"),
            "series": reverse("media:series_list"),
            "anime": reverse("media:anime_list")
        }

        if "media" in self.request.GET:
            media_query = self.request.GET["media"]
            media_name = media_query if media_query in media_dict else "book"
            self.request.session["genre_media"] = media_name
        elif "genre_media" in self.request.session.keys():
            media_name = self.request.session["genre_media"]
        else:
            media_name = "book"

        context["redirect_url"] = media_dict[media_name]
        context["media"] = media_name
        context["query_params"] = self.request.GET.copy()
        return context

    def get_queryset(self):
        queryset = Genre.objects.all()
        form = GenreSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class BookListView(LoginRequiredMixin, MediaListMixin, generic.ListView):
    model = Book
    paginate_by = 10
    template_name = "media/book-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["type_choices"] = [
            choice_type[1]
            for choice_type in Book.type.field.choices
        ]
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        type_choice = self.request.GET.get("type")
        db_stored_choice = get_reverse_choice(type_choice, Book.type)
        if db_stored_choice:
            queryset = queryset.filter(
                type=db_stored_choice
            )
        return queryset


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = "media/detail/book-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = "book"
        context["delete_url"] = reverse_lazy(
            "media:book_delete",
            args=[context["book"].id]
        )
        return context


class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy("media:book_list")


class BookCreateView(LoginRequiredMixin, BookMutateMixin, generic.CreateView):
    success_url = reverse_lazy("media:book_list")

class BookUpdateView(LoginRequiredMixin, BookMutateMixin, generic.UpdateView):
    def get_success_url(self):
        self.success_url = reverse_lazy("media:book_detail", kwargs={"pk": self.object.id})
        return super().get_success_url()

class FilmListView(LoginRequiredMixin, MediaListMixin, generic.ListView):
    model = Film
    paginate_by = 10
    template_name = "media/film-list.html"


class FilmDetailView(LoginRequiredMixin, generic.DetailView):
    model = Film
    template_name = "media/detail/film-detail.html"

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
