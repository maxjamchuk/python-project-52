from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from task_manager.users.forms import CustomAuthenticationForm
from task_manager.views import IndexView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("users/", include("task_manager.users.urls")),
    path("", include("task_manager.users.auth_urls")),
    path("statuses/", include("task_manager.statuses.urls")),
    path("tasks/", include("task_manager.tasks.urls")),
    path("labels/", include("task_manager.labels.urls")),

    path(
        "login/",
        LoginView.as_view(
            template_name="auth/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]
