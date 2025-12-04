from django.contrib import admin
from django.urls import include, path

from .views import IndexView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("users/", include("task_manager.users.urls")),
    path("", include("task_manager.users.auth_urls")),
    path("statuses/", include("task_manager.statuses.urls")),
    path("tasks/", include("task_manager.tasks.urls")),
    path("labels/", include("task_manager.labels.urls")),
]
