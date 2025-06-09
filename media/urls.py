from django.urls import path

from media.views.views import (
    index, GenreListView,
    BookListView, BookDetailView,
    BookDeleteView, BookCreateView,
    BookUpdateView, FilmListView, FilmCreateView,
    FilmDetailView, FilmDeleteView, FilmUpdateView
)

urlpatterns = [
    path("", index, name="index"),
    path("genres/", GenreListView.as_view(), name="genre_list"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path(
        "books/<int:pk>/delete/",
        BookDeleteView.as_view(),
        name="book_delete"
    ),
    path(
        "books/<int:pk>/update/",
        BookUpdateView.as_view(),
        name="book_update"
    ),
    path("books/create/", BookCreateView.as_view(), name="book_create"),
    path("comics/", GenreListView.as_view(), name="comic_list"),
    path("series/", GenreListView.as_view(), name="series_list"),
    path("films/", FilmListView.as_view(), name="film_list"),
    path("films/create/", FilmCreateView.as_view(), name="film_create"),
    path("films/<int:pk>/", FilmDetailView.as_view(), name="film_detail"),
    path(
        "films/<int:pk>/delete/",
        FilmDeleteView.as_view(),
        name="film_delete"
    ),
path(
        "films/<int:pk>/update/",
        FilmUpdateView.as_view(),
        name="film_update"
    ),
    path("anime/", GenreListView.as_view(), name="anime_list")
]

app_name = "media"
