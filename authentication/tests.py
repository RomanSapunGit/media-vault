from django.test import TestCase
from django.urls import reverse


class RegisterViewTests(TestCase):
    def test_user_register_valid(self):
        response = self.client.post(
            reverse("authentication:register"),
            data={
                "username": "user1",
                "email": "user@user.com",
                "password1": "%amgf83501767",
                "password2": "%amgf83501767"
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_user_register_invalid(self):
        response = self.client.post(
            reverse("authentication:register"),
            data={
                "username": "user1",
                "email": "user@user.com",
                "password1": "123",
                "password2": "%amgf83501767"
            }
        )
        print(response.context["form"])
        self.assertFalse(response.context["form"].is_valid())

        self.assertEqual(
            response.context["form"].errors,
            {"password2": ["The two password fields didn’t match."]}
        )
