
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("media.urls", namespace="media")),
    path("auth/", include("authentication.urls", namespace="authentication")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()
