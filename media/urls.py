from django.urls import path

from media.views.book_views import (
    BookListView, BookDetailView,
    BookDeleteView, BookUpdateView,
    BookCreateView
)
from media.views.film_views import (
    FilmListView, FilmCreateView,
    FilmDetailView, FilmDeleteView,
    FilmUpdateView
)
from media.views.series_views import (
    SeriesListView, SeriesCreateView,
    SeriesDetailView, SeriesDeleteView,
    SeriesUpdateView
)
from media.views.user_views import (
    UserListView, UserDetailView,
    UserDeleteView, UserUpdateView
)
from media.views.views import (
    index, GenreListView,
    CreatorListView, CreatorCreateView,
    CreatorDeleteView, CreatorUpdateView
)
from media.views.rating_views import (
    RatingListView, RatingDetailView,
    RatingDeleteView, RatingUpdateView,
    RatingCreateView
)

urlpatterns = [
    path("", index, name="index"),
    path("genres/", GenreListView.as_view(), name="genre_list"),
    path("creators/", CreatorListView.as_view(), name="creator_list"),
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
    path("series/", SeriesListView.as_view(), name="series_list"),
    path("series/create/", SeriesCreateView.as_view(), name="series_create"),
    path("series/<int:pk>/", SeriesDetailView.as_view(), name="series_detail"),
    path(
        "series/<int:pk>/delete/",
        SeriesDeleteView.as_view(),
        name="series_delete"
    ),
    path(
        "series/<int:pk>/update/",
        SeriesUpdateView.as_view(),
        name="series_update"
    ),
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
    path("users/", UserListView.as_view(), name="user_list"),
    path(
        "users/<int:pk>/",
        UserDetailView.as_view(),
        name="user_detail"
    ),
    path(
        "users/<int:pk>/delete",
        UserDeleteView.as_view(),
        name="user_delete"
    ),
    path(
        "users/<int:pk>/update",
        UserUpdateView.as_view(),
        name="user_update"
    ),
    path("ratings/", RatingListView.as_view(), name="rating_list"),
    path(
        "ratings/<int:pk>/",
        RatingDetailView.as_view(),
        name="rating_detail"
    ),
    path(
        "ratings/<int:pk>/delete/",
        RatingDeleteView.as_view(),
        name="rating_delete"
    ),
    path(
        "ratings/<int:pk>/update",
        RatingUpdateView.as_view(),
        name="rating_update"
    ),
    path(
        "ratings/create/",
        RatingCreateView.as_view(),
        name="rating_create"
    ),
    path(
        "creators/create/",
        CreatorCreateView.as_view(),
        name="creator_create"
    ),
    path(
        "creators/<int:pk>/delete/",
        CreatorDeleteView.as_view(),
        name="creator_delete"
    ),
]

app_name = "media"
