from django.contrib import admin
from django.urls import include, path

from .views import IndexView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("users/", include("users.urls")),
    path("", include("users.auth_urls")),
]
