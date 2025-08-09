import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from media.models import Book, Film, Series, UserMediaRating, Creator

GENRES = "genres"
CREATORS = "creators"
TYPE = "type"


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
        "those insights to show us how to give our animals "
        "the best and happiest "
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
            f"{reverse(self.BOOK_LIST_URL_NAME)}?title="
            f"Harry+Potter+and+the+Philosopher's+Stone"
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
            f"{reverse(self.BOOK_LIST_URL_NAME)}?{TYPE}={self.TYPE_COMICS}"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?{GENRES}={self.GENRE_FANTASY}"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?"
            f"{CREATORS}={self.CREATOR_JOANNE}"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?{TYPE}={self.TYPE_INVALID}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context[self.BOOK_LIST]), [])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?"
            f"{GENRES}={self.GENRE_FANTASY}"
            f"&{CREATORS}={self.CREATOR_JOANNE}"
        )
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?"
            f"{GENRES}={self.GENRE_FANTASY}"
            f"&{CREATORS}={self.CREATOR_GEORGE}"
        )
        creators_form = response.context["creators_filter_form"]
        self.assertFalse(creators_form.is_valid())
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

        response = self.client.get(
            f"{reverse(self.BOOK_LIST_URL_NAME)}?"
            f"{GENRES}={self.GENRE_HORROR}&"
            f"{CREATORS}={self.CREATOR_JOANNE}"
        )
        genre_form = response.context["genre_filter_form"]
        self.assertFalse(genre_form.is_valid())
        self.assertEqual(list(response.context[self.BOOK_LIST]), [book])

    def test_create_book(self):
        response = self.client.post(
            reverse(self.BOOK_CREATE_URL_NAME), self.data
        )
        self.assertIsNotNone(response.context["form"].errors)

        self.data.update({GENRES: 1})
        response = self.client.post(
            reverse(self.BOOK_CREATE_URL_NAME), self.data
        )

        self.assertEqual(response.status_code, 302)
        created_book = Book.objects.get(title=self.BOOK_TITLE)
        self.assertIsNotNone(created_book)

        self.data.pop(GENRES)

    def test_book_mixin_sets_type_in_query_param(self):
        response = self.client.get(
            f"{reverse(self.BOOK_CREATE_URL_NAME)}?{TYPE}={self.TYPE_COMICS}"
        )
        self.assertEqual(
            self.TYPE_CS, response.context["form"].initial.get(TYPE)
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
    USERNAME = "user"
    PASSWORD = "password"
    COUNTRY_USA = "USA"
    COUNTRY_UK = "UK"
    GENRE_VALID = "Science Fiction"
    GENRE_INVALID = "Horror"
    CREATOR_VALID = "Isaac"
    CREATOR_INVALID = "George"
    INVALID_TYPE = "wrong type"
    VALID_TITLE_SEARCH = "I,+Robot"
    INVALID_TITLE_SEARCH = "7"
    CREATED_AT = datetime.date(2009, 1, 6)
    DURATION = datetime.time(1, 40)
    UPDATED_DURATION = datetime.time(2, 21)
    FILM_LIST = "film_list"
    FILM_LIST_URL_NAME = "media:film_list"
    FILM_TITLE = (
        "Animals Make Us Human: Creating the Best Life for Animals"
    )
    FILM_DESCRIPTION = (
        "In her groundbreaking and best-selling book Animals in Translation, "
        "Temple Grandin drew on her own experience with autism as well as her "
        "distinguished career as an animal scientist to deliver extraordinary "
        "insights into how animals think, act, and feel. Now she builds on "
        "those insights to show us how to give our animals the best and "
        "happiest life on their terms, not ours."
    )

    fixtures = ["media_vault_db_data.json"]

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD
        )
        self.user = user
        self.client.force_login(user)

        self.data = {
            "title": self.FILM_TITLE,
            "description": self.FILM_DESCRIPTION,
            "created_at": self.CREATED_AT,
            "created_by": self.USERNAME,
            "country": self.COUNTRY_USA,
            "duration": self.DURATION
        }

    def test_film_list_exact(self):
        response = self.client.get(reverse(self.FILM_LIST_URL_NAME))
        self.assertEqual(response.status_code, 200)

        film = Film.objects.get(pk=1)
        self.assertEqual(
            list(response.context[self.FILM_LIST]), [film]
        )

    def test_film_list_search(self):
        response = self.client.get(
            f"{reverse(self.FILM_LIST_URL_NAME)}"
            f"?title={self.INVALID_TITLE_SEARCH}"
        )
        self.assertEqual(response.status_code, 200)
        film = Film.objects.get(pk=1)
        self.assertNotEqual(list(response.context[self.FILM_LIST]), [film])

        response = self.client.get(
            f"{reverse(self.FILM_LIST_URL_NAME)}"
            f"?title={self.VALID_TITLE_SEARCH}"
        )
        self.assertEqual(list(response.context[self.FILM_LIST]), [film])

    def test_film_list_filter(self):
        new_film = Film(**self.data)
        new_film.save()
        film = Film.objects.get(pk=1)

        response = self.client.get(reverse(self.FILM_LIST_URL_NAME))
        self.assertIn(new_film, list(response.context[self.FILM_LIST]))
        self.assertIn("genre_filter_form", response.context)
        self.assertIn("creators_filter_form", response.context)

        response = self.client.get(
            f"{reverse(self.FILM_LIST_URL_NAME)}?{GENRES}={self.GENRE_VALID}"
        )
        self.assertEqual(list(response.context[self.FILM_LIST]), [film])

        response = self.client.get(
            f"{reverse(self.FILM_LIST_URL_NAME)}"
            f"?{CREATORS}={self.CREATOR_VALID}"
        )
        self.assertEqual(list(response.context[self.FILM_LIST]), [film])

        response = self.client.get(
            f"{reverse(self.FILM_LIST_URL_NAME)}"
            f"?{GENRES}={self.GENRE_VALID}"
            f"&{CREATORS}={self.CREATOR_VALID}"
        )
        self.assertEqual(
            list(response.context[self.FILM_LIST]), [film]
        )

        response = self.client.get(
            f"{reverse(self.FILM_LIST_URL_NAME)}"
            f"?{GENRES}={self.GENRE_VALID}"
            f"&{CREATORS}={self.CREATOR_INVALID}"
        )
        creators_form = response.context["creators_filter_form"]
        self.assertFalse(creators_form.is_valid())
        self.assertEqual(list(response.context[self.FILM_LIST]), [film])

        response = self.client.get(
            f"{reverse(self.FILM_LIST_URL_NAME)}"
            f"?{GENRES}={self.GENRE_INVALID}"
            f"&{CREATORS}={self.CREATOR_VALID}"
        )
        genre_form = response.context["genre_filter_form"]
        self.assertFalse(genre_form.is_valid())
        self.assertEqual(list(response.context[self.FILM_LIST]), [film])

    def test_create_film(self):
        response = self.client.post(
            reverse("media:film_create"),
            self.data
        )
        self.assertIsNotNone(response.context["form"].errors)

        self.data.update({GENRES: 1})
        response = self.client.post(
            reverse("media:film_create"),
            self.data
        )
        self.assertEqual(response.status_code, 302)
        created_film = Film.objects.get(title=self.FILM_TITLE)
        self.assertIsNotNone(created_film)
        self.data.pop(GENRES)

    def test_film_mixin_sets_type_in_query_param(self):
        response = self.client.get(
            f"{reverse('media:book_create')}?{CREATORS}={self.CREATOR_VALID}"
        )
        self.assertEqual(
            [1],
            list(response.context["form"].initial.get(CREATORS))
        )

    def test_film_update_view(self):
        film = Film.objects.get(pk=1)
        response = self.client.post(
            reverse("media:film_update", args=[film.pk]),
            {
                "title": "Updated Title",
                "description": film.description,
                "created_at": film.created_at,
                "created_by": film.created_by,
                "country": self.COUNTRY_UK,
                "duration": self.UPDATED_DURATION,
                "genres": 1
            }
        )
        self.assertEqual(response.status_code, 302)
        film.refresh_from_db()
        self.assertEqual(film.title, "Updated Title")


class PrivateSeriesViewTests(TestCase):
    fixtures = ["media_vault_db_data.json"]

    CONTEXT_FORM = "form"
    CONTEXT_STATUS_CHOICES = "status_choices"
    CONTEXT_SERIES_LIST = "series_list"

    URL_SERIES_LIST = "media:series_list"
    URL_SERIES_UPDATE = "media:series_update"

    QUERY_PARAM_STATUS = "status"

    STATUS_FINISHED = "Finished"
    STATUS_IN_PROGRESS = "In progress"
    STATUS_DROPPED = "Dropped"
    STATUS_DB_VALUE = "F"

    TYPE_ANIME = "Anime"
    TYPE_DB_VALUE = "AE"

    data = {
        "title": "Attack on Titan",
        "description": (
            "In a world where humanity is on the brink of extinction, "
            "young soldiers fight giant humanoid creatures known as Titans."
        ),
        "created_at": "2013-04-07",
        "created_by": "bob",
        "media_type": "Series",
        "seasons": 4,
        "series_number": 48
    }

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="user", password="password"
        )
        self.user = user
        self.client.force_login(user)

    def test_series_list_filter(self):
        new_series = Series(**self.data)
        new_series.save()

        url = (
            f"{reverse(self.URL_SERIES_LIST)}"
            f"?{self.QUERY_PARAM_STATUS}={self.STATUS_FINISHED}"
        )
        response = self.client.get(url)

        self.assertNotEqual(
            list(response.context[self.CONTEXT_SERIES_LIST]), []
        )
        self.assertNotIn(
            new_series, response.context[self.CONTEXT_SERIES_LIST]
        )

    def test_context_set_correctly(self):
        expected_statuses = [
            self.STATUS_FINISHED,
            self.STATUS_IN_PROGRESS,
            self.STATUS_DROPPED,
        ]

        response = self.client.get(reverse(self.URL_SERIES_LIST))
        self.assertEqual(
            expected_statuses,
            response.context[self.CONTEXT_STATUS_CHOICES]
        )

    def test_series_update_sets_status_and_type_correctly(self):
        url = reverse(self.URL_SERIES_UPDATE, kwargs={"pk": 2})
        url += (
            f"?{TYPE}={self.TYPE_ANIME}"
            f"&{self.QUERY_PARAM_STATUS}={self.STATUS_FINISHED}"
        )

        response = self.client.get(url)

        form_initial = response.context[self.CONTEXT_FORM].initial
        self.assertEqual(self.TYPE_DB_VALUE, form_initial.get(TYPE))
        self.assertEqual(
            self.STATUS_DB_VALUE, form_initial.get(self.QUERY_PARAM_STATUS)
        )


class PrivateRatingViewTests(TestCase):
    fixtures = ["media_vault_db_data.json"]

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="user", password="password"
        )
        self.user = user
        self.client.force_login(user)

    def test_rating_delete_view_success_url(self):
        response = self.client.post(
            reverse('media:rating_delete', kwargs={'pk': 1}),
            data={"next": "/users/1/"}
        )
        self.assertEqual(response.url, "/users/1/")

        response = self.client.post(
            reverse('media:rating_delete', kwargs={'pk': 2})
        )
        self.assertEqual(response.url, "/ratings/")

    def test_rating_update_success_url_with_next_param(self):
        rating = UserMediaRating.objects.get(pk=1)
        url = reverse(
            "media:rating_update",
            kwargs={"pk": rating.pk}
        )
        response = self.client.post(
            f"{url}?next=/&user_id={self.user.pk}",
            {
                "rating": 5.0,
                "media": 1
            }
        )
        rating.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("media:user_detail", args=[self.user.pk])
        )
        self.assertEqual(rating.rating, 5)

    def test_rating_update_success_url_without_next_param(self):
        rating = UserMediaRating.objects.get(pk=1)
        url = reverse("media:rating_update", kwargs={"pk": rating.pk})
        response = self.client.post(
            url,
            {
                "rating": 3.0,
                "media": 1
            }
        )

        rating.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("media:rating_detail", args=[rating.pk])
        )
        self.assertEqual(rating.rating, 3)


class PrivateUserViewTests(TestCase):
    fixtures = ["media_vault_db_data.json"]
    USER_LIST = "user_list"

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="user", password="password"
        )
        self.user = user
        self.client.force_login(user)

    def test_user_search_filters_correctly(self):
        response = self.client.get(
            f"{reverse('media:user_list')}?username=Tom"
        )
        all_users = UserMediaRating.objects.all()

        self.assertNotEqual(response.context[self.USER_LIST], all_users)
        self.assertEqual(len(response.context[self.USER_LIST]), 1)

    def test_detail_view_not_shows_hidden_ratings(self):
        response = self.client.get(reverse(
            "media:user_detail",
            kwargs={"pk": 1})
        )
        user = response.context["object"]

        for media_rating in user.media_ratings.all():
            self.assertFalse(media_rating.is_hidden)


class PrivateViewTests(TestCase):
    fixtures = ["media_vault_db_data.json"]

    INDEX_URL = reverse("media:index")
    CREATOR_CREATE_URL = reverse("media:creator_create")
    CREATOR_LIST_URL = reverse("media:creator_list")
    JSON_TYPE = "application/json"

    VALID_CREATOR_DATA = {
        "first_name": "New",
        "last_name": "Creator",
        "birth_date": datetime.date(2000, 12, 2)
    }

    REQUIRED_FIELD_ERRORS = [
        "The field First name is required",
        "The field Last name is required",
        "The field Birth date is required"
    ]

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="user", password="password"
        )
        self.user = user
        self.client.force_login(user)

    def test_index_shows_count_correctly(self):
        response = self.client.get(self.INDEX_URL)
        self.assertEqual(response.context["media_users_count"], 3)
        self.assertEqual(response.context["media_titles_count"], 3)
        self.assertEqual(response.context["media_ratings_count"], 3)

    def test_creator_create_view_success(self):
        response = self.client.post(
            self.CREATOR_CREATE_URL,
            data=self.VALID_CREATOR_DATA
        )
        self.assertRedirects(response, self.CREATOR_LIST_URL)
        self.assertTrue(Creator.objects.filter(first_name="New").exists())

    def test_creator_create_view_failure(self):
        invalid_data = self.VALID_CREATOR_DATA.copy()
        invalid_data.pop("last_name")
        response = self.client.post(self.CREATOR_CREATE_URL, data=invalid_data)
        self.assertFalse(response.context["form"].is_valid())

    def test_creator_create_view_ajax_valid(self):
        response = self.client.post(
            self.CREATOR_CREATE_URL,
            data=self.VALID_CREATOR_DATA,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], self.JSON_TYPE)

        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertIn("author", json_data)
        self.assertEqual(json_data["author"]["name"], "New Creator")

    def test_creator_create_view_ajax_invalid(self):
        response = self.client.post(
            self.CREATOR_CREATE_URL,
            data={},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], self.JSON_TYPE)

        json_data = response.json()
        self.assertFalse(json_data["success"])
        self.assertIn("form_html", json_data)

        for error in self.REQUIRED_FIELD_ERRORS:
            self.assertIn(error, json_data["form_html"])
