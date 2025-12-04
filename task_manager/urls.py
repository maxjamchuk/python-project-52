from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from task_manager.users.forms import CustomAuthenticationForm
from task_manager.users.views import CustomLoginView, CustomLogoutView
from task_manager.views import IndexView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("users/", include("task_manager.users.urls")),
    path("statuses/", include("task_manager.statuses.urls", namespace="statuses")),
    path("tasks/", include("task_manager.tasks.urls")),
    path("labels/", include("task_manager.labels.urls")),

    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
