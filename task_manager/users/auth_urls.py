from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomAuthenticationForm

app_name = "users_auth"

urlpatterns = [
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
