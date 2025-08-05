from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from media.models import Book


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


class PrivateViewTests(TestCase):
    fixtures = ["media_vault_db_data.json"]

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="user", password="password"
        )
        self.client.force_login(user)

    def test_book_list_exact(self):
        response = self.client.get(reverse("media:book_list"))
        self.assertEqual(response.status_code, 200)

        book = Book.objects.get(pk=3)
        self.assertEqual(list(response.context["book_list"]), [book])

    def test_book_list_search(self):
        response = self.client.get(f"{reverse('media:book_list')}?title=7")
        self.assertEqual(response.status_code, 200)

        book = Book.objects.get(pk=3)

        self.assertNotEqual(list(response.context["book_list"]), [book])

        response = self.client.get(f"{reverse('media:book_list')}?title="
                                   f"Harry Potter and the Philosopher's Stone")

        self.assertEqual(list(response.context["book_list"]), [book])

    def test_book_list_filter_with_wrong_query_shows_all_books(self):
        response = self.client.get(f"{reverse('media:book_list')}?type=wrong+type")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context["book_list"]), [])

    def test_book_list_filter(self):
        new_book = Book(**self.data)
        new_book.save()
        book = Book.objects.get(pk=3)

        response = self.client.get(f"{reverse('media:book_list')}?type=Comics")
        self.assertEqual(list(response.context["book_list"]), [])

        response = self.client.get(f"{reverse('media:book_list')}?genres=Fantasy")
        self.assertEqual(list(response.context["book_list"]), [book])

        response = self.client.get(f"{reverse('media:book_list')}?creators=Joanne")
        self.assertEqual(list(response.context["book_list"]), [book])

    def test_create_book(self):

        response = self.client.post(
            reverse("media:book_create"),
            self.data
        )
        self.assertIsNotNone(response.context["form"].errors)

        self.data.update({"genres": 1})
        response = self.client.post(
            reverse("media:book_create"),
            self.data
        )

        self.assertEqual(response.status_code, 302)
        created_book = Book.objects.get(title=self.BOOK_TITLE)
        self.assertIsNotNone(created_book)

    def test_create_book_with_initial(self):
        response = self.client.get(
            f"{reverse('media:book_create')}?type=Comics"
        )
        self.assertEqual(
            "CS",
            response.context["form"].initial.get("type")
        )
