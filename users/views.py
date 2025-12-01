from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import UserRegistrationForm, UserUpdateForm

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, _("User has been successfully registered"))
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs.get("pk"):
            messages.error(self.request, _("You have no rights to edit this user"))
            return redirect("users:list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _("User has been successfully updated"))
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs.get("pk"):
            messages.error(self.request, _("You have no rights to delete this user"))
            return redirect("users:list")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(self.request, _("User has been successfully deleted"))
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request,
                _("It is not possible to delete a user because it is in use"),
            )
            return redirect("users:list")


class UserLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    http_method_names = ["post"]
