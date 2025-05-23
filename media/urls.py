from django.urls import path

from media.views import (index, GenreListView, )

urlpatterns = [
    path("", index, name="index"),
    path("genres/", GenreListView.as_view(), name="genre_list"),
    path("books/", GenreListView.as_view(), name="book_list"),
    path("comics/", GenreListView.as_view(), name="comic_list"),
    path("series/", GenreListView.as_view(), name="series_list"),
    path("films/", GenreListView.as_view(), name="film_list"),
    path("anime/", GenreListView.as_view(), name="anime_list")
]

app_name = "media"
