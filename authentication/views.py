from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from authentication.forms import SignUpForm, MediaUserLoginForm
from media.models import MediaUser


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user:
                return render(request,"home/index.html")
        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(
        request, "account/register.html", {"form": form, "msg": msg, "success": success}
    )


class UserLoginView(LoginView):
    model = MediaUser
    template_name = "account/login.html"
    form_class = MediaUserLoginForm
