import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from media.models import Book, Film


class PublicTests(TestCase):
    def test_books_anonymous_access_false(self):
        response = self.client.get("/books/")
        self.assertNotEqual(response.status_code, 200)

    def test_films_anonymous_access_false(self):
        response = self.client.get("/films/")
        self.assertNotEqual(response.status_code, 200)

    def test_series_anonymous_access_false(self):
        response = self.client.get("/series/")
        self.assertNotEqual(response.status_code, 200)

    def test_users_anonymous_access_false(self):
        response = self.client.get("/users/")
        self.assertNotEqual(response.status_code, 200)

    def test_ratings_anonymous_access_false(self):
        response = self.client.get("/ratings/")
        self.assertNotEqual(response.status_code, 200)

    def test_genres_anonymous_access_false(self):
        response = self.client.get("/genres/")
        self.assertNotEqual(response.status_code, 200)

    def test_creators_anonymous_access_false(self):
        response = self.client.get("/creators/")
        self.assertNotEqual(response.status_code, 200)


class PrivateBookViewTests(TestCase):
    BOOK_TITLE = (
        "Animals Make Us Human: Creating the Best Life for Animals"
    )
    BOOK_DESCRIPTION = (
        "In her groundbreaking and best-selling book Animals in Translation, "
        "Temple Grandin drew on her own experience with autism as well as her "
        "distinguished career as an animal scientist to deliver extraordinary "
        "insights into how animals think, act, and feel. Now she builds on "
        "those insights to show us how to give our animals the best and happiest "
        "life on their terms, not ours."
    )
    BOOK_CREATED_AT = datetime.date(2009, 1, 6)

    BOOK_LIST_URL_NAME = "media:book_list"
    BOOK_CREATE_URL_NAME = "media:book_create"
    BOOK_UPDATE_URL_NAME = "media:book_update"
    BOOK_PK = 3

    GENRE_FANTASY = "Fantasy"
    GENRE_HORROR = "Horror"
    CREATOR_JOANNE = "Joanne"
    CREATOR_GEORGE = "George"
    TYPE_COMICS = "Comics"
    TYPE_INVALID = "wrong type"
    TYPE_CS = "CS"
    GENRES = "genres"
    CREATORS = "creators"
    TYPE = "type"
    BOOK_LIST = "book_list"

    fixtures = ["media_vault_db_data.json"]

    data = {
        "title": BOOK_TITLE,
        "description": BOOK_DESCRIPTION,
        "created_at": BOOK_CREATED_AT,
        "created_by": "user",
        "chapters": 1,
        "type": "TB",
    }

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="user", password="password"
        )
        self.user = user
        self.client.force_login(user)

    def test_book_list_exact(self):
        response = self.client.get(reverse(self.BOOK_LIST_URL_NAME))
        self.assertEqual(response.status_code, 200)

        book = Book.objects.get(pk=self.BOOK_PK)
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

    def test_book_list_search(self):
        book = Book.objects.get(pk=self.BOOK_PK)

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?title=7"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?title=Harry+Potter+and+the+Philosopher's+Stone"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

    def test_book_list_filter(self):
        new_book = Book(**self.data)
        new_book.save()
        book = Book.objects.get(pk=self.BOOK_PK)

        response = self.client.get(reverse(self.BOOK_LIST_URL_NAME))
        self.assertIn(new_book, list(response.context[self.BOOK_LIST]))

        self.assertIn("genre_filter_form", response.context)
        self.assertIn("creators_filter_form", response.context)

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?{self.TYPE}={self.TYPE_COMICS}"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?{self.GENRES}={self.GENRE_FANTASY}"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?{self.CREATORS}={self.CREATOR_JOANNE}"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?{self.TYPE}={self.TYPE_INVALID}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context[self.BOOK_LIST]), [])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?"
            f"{self.GENRES}={self.GENRE_FANTASY}"
            f"&{self.CREATORS}={self.CREATOR_JOANNE}"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?"
            f"{self.GENRES}={self.GENRE_FANTASY}"
            f"&{self.CREATORS}={self.CREATOR_GEORGE}"
        )
        creators_form = response.context["creators_filter_form"]
        self.assertFalse(creators_form.is_valid())
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?"
            f"{self.GENRES}={self.GENRE_HORROR}&"
            f"{self.CREATORS}={self.CREATOR_JOANNE}"
        )
        genre_form = response.context["genre_filter_form"]
        self.assertFalse(genre_form.is_valid())
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

    def test_create_book(self):
        response = self.client.post(reverse(self.BOOK_CREATE_URL_NAME), self.data)
        self.assertIsNotNone(response.context["form"].errors)

        self.data.update({self.GENRES: 1})
        response = self.client.post(reverse(self.BOOK_CREATE_URL_NAME), self.data)

        self.assertEqual(response.status_code, 302)
        created_book = Book.objects.get(title=self.BOOK_TITLE)
        self.assertIsNotNone(created_book)

        self.data.pop(self.GENRES)

    def test_book_mixin_sets_type_in_query_param(self):
        response = self.client.get(
            f"{reverse(self.BOOK_CREATE_URL_NAME)}?{self.TYPE}={self.TYPE_COMICS}"
        )
        self.assertEqual(
            self.TYPE_CS, response.context["form"].initial.get(self.TYPE)
        )

    def test_book_update_view(self):
        book = Book.objects.get(pk=self.BOOK_PK)
        response = self.client.post(
            reverse(self.BOOK_UPDATE_URL_NAME, args=[book.pk]),
            {
                "title": "Updated Title",
                "description": book.description,
                "created_at": book.created_at,
                "created_by": book.created_by,
                "chapters": book.chapters,
                "type": book.type,
                "genres": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        book.refresh_from_db()
        self.assertEqual(book.title, "Updated Title")


class PrivateFilmViewTests(TestCase):
    FILM_TITLE = ("Animals Make Us Human: "
                  "Creating the Best Life for Animals")
    FILM_DESCRIPTION = ("In her groundbreaking and "
                        "best-selling book Animals in Translation, "
                        "Temple Grandin drew on her own experience "
                        "with autism as well as her distinguished "
                        "career as an animal scientist to deliver "
                        "extraordinary insights into how animals "
                        "think, act, and feel. Now she builds on "
                        "those insights to show us how to give "
                        "our animals the best and happiest "
                        "life on their terms, not ours.")
    FILM_CREATED_AT = datetime.date(2009, 1, 6)

    data = {
        "title": FILM_TITLE,
        "description": FILM_DESCRIPTION,
        "created_at": FILM_CREATED_AT,
        "created_by": "user",
        "country": "USA",
        "duration": datetime.time(1, 40)
    }

    fixtures = ["media_vault_db_data.json"]

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="user", password="password"
        )
        self.user = user
        self.client.force_login(user)

    def test_film_list_exact(self):
        response = self.client.get(reverse("media:film_list"))
        self.assertEqual(response.status_code, 200)

        film = Film.objects.get(pk=1)
        self.assertEqual(list(response.context["film_list"]), [film])

    def test_film_list_search(self):
        response = self.client.get(f"{reverse('media:film_list')}?title=7")
        self.assertEqual(response.status_code, 200)

        film = Film.objects.get(pk=1)

        self.assertNotEqual(list(response.context["film_list"]), [film])

        response = self.client.get(f"{reverse('media:film_list')}?title="
                                   f"I,+Robot")

        self.assertEqual(list(response.context["film_list"]), [film])

    def test_film_list_filter_with_wrong_query_shows_all_films(self):
        response = self.client.get(f"{reverse('media:film_list')}?type=wrong+type")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context["film_list"]), [])

    def test_book_list_filter(self):
        new_film = Film(**self.data)
        new_film.save()
        film = Film.objects.get(pk=1)

        response = self.client.get(reverse("media:film_list"))
        self.assertIn(new_film, list(response.context["film_list"]))

        self.assertIn("genre_filter_form", response.context)
        self.assertIn("creators_filter_form", response.context)

        response = self.client.get(f"{reverse('media:film_list')}?genres=Science+Fiction")
        self.assertEqual(list(response.context["film_list"]), [film])

        response = self.client.get(f"{reverse('media:film_list')}?creators=Isaac")
        self.assertEqual(list(response.context["film_list"]), [film])

        response = self.client.get(f"{reverse('media:film_list')}?genres=Science+Fiction&creators=Isaac")
        self.assertEqual(list(response.context["film_list"]), [film])

        response = self.client.get(f"{reverse('media:film_list')}?genres=Science+Fiction&creators=George")
        creators_form = response.context["creators_filter_form"]
        self.assertFalse(creators_form.is_valid())
        self.assertEqual(list(response.context["film_list"]), [film])

        response = self.client.get(f"{reverse('media:film_list')}?genres=Horror&creators=Isaac")
        creators_form = response.context["genre_filter_form"]
        self.assertFalse(creators_form.is_valid())
        self.assertEqual(list(response.context["film_list"]), [film])

    def test_create_film(self):
        response = self.client.post(
            reverse("media:film_create"),
            self.data
        )
        self.assertIsNotNone(response.context["form"].errors)

        self.data.update({"genres": 1})
        response = self.client.post(
            reverse("media:film_create"),
            self.data
        )

        self.assertEqual(response.status_code, 302)
        created_film = Film.objects.get(title=self.FILM_TITLE)
        self.assertIsNotNone(created_film)

        self.data.pop("genres")

    def test_film_mixin_sets_type_in_query_param(self):
        response = self.client.get(
            f"{reverse('media:book_create')}?creators=Isaac"
        )
        self.assertEqual(
            [1],
            list(response.context["form"].initial.get("creators"))
        )

    def test_film_update_view(self):
        film = Film.objects.get(pk=1)
        response = self.client.post(
            reverse("media:film_update", args=[film.pk]),
            {"title": "Updated Title", "description": film.description,
             "created_at": film.created_at, "created_by": film.created_by,
             "country": "UK", "duration": datetime.time(2, 21), "genres": 1}
        )
        self.assertEqual(response.status_code, 302)
        film.refresh_from_db()
        self.assertEqual(film.title, "Updated Title")
