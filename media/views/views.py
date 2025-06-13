from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from media.forms.forms import (
    GenreSearchForm, UserSearchForm, MediaUserUpdateForm,
)
from media.models import Genre, Book, Film, Series, Media, MediaUser
from media.utils import get_reverse_choice
from media.views.mixins import (
    BookMutateMixin, FilmMutateMixin,
    MediaListMixin, SeriesMutateMixin
)


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    media_users_count = get_user_model().objects.count()
    context = {
        "media_users_count": media_users_count,
        "media_titles_count": Media.objects.all().count()
    }
    return render(request, "home/index.html", context)


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name = "media/list/genre-list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["search_form"] = GenreSearchForm(self.request.GET)

        media_dict = {
            "book": reverse("media:book_list"),
            "film": reverse("media:film_list"),
            "comic": reverse("media:comic_list"),
            "series": reverse("media:series_list"),
            "anime": f"{reverse('media:series_list')}?type=Anime"
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
    template_name = "media/list/book-list.html"

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
        self.success_url = reverse_lazy(
            "media:book_detail", kwargs={"pk": self.object.id}
        )
        return super().get_success_url()


class FilmListView(LoginRequiredMixin, MediaListMixin, generic.ListView):
    model = Film
    paginate_by = 10
    template_name = "media/list/film-list.html"


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


class SeriesListView(LoginRequiredMixin, MediaListMixin, generic.ListView):
    model = Series
    paginate_by = 10
    template_name = "media/list/series-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["type_choices"] = [
            choice_type[1]
            for choice_type in Series.type.field.choices
        ]
        context["status_choices"] = [
            choice_status[1]
            for choice_status in Series.status.field.choices
        ]
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        type_choice = self.request.GET.get("type")
        db_stored_choice = get_reverse_choice(type_choice, Series.type)
        if db_stored_choice:
            queryset = queryset.filter(
                type=db_stored_choice
            )
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
    template_name = "media/detail/series-detail.html"

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


class UserListView(LoginRequiredMixin, generic.ListView):
    model = MediaUser
    paginate_by = 10
    template_name = "media/list/users-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["query_params"] = self.request.GET.copy()
        context["search_form"] = UserSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_form = UserSearchForm(self.request.GET)
        if search_form.is_valid():
            queryset = queryset.filter(
                username__icontains=search_form.cleaned_data["username"]
            )
        return queryset


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = MediaUser
    template_name = "media/detail/user-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = "user"
        context["delete_url"] = reverse_lazy(
            "media:user_delete",
            args=[context["mediauser"].id]
        )
        return context


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = MediaUser
    success_url = reverse_lazy("media:user_list")


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = MediaUser
    template_name = "media/form/media-form.html"
    form_class = MediaUserUpdateForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def get_success_url(self):
        logout(self.request)
        return reverse_lazy("authentication:login")
