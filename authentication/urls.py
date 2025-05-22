from django.urls import path

from authentication.views import (UserLoginView,
                                  register_user)

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
]

app_name = "authentication"
