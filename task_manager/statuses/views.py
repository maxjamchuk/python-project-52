from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ("name",)
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:list")

    def form_valid(self, form):
        messages.success(self.request, _("Статус успешно создан"))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ("name",)
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:list")

    def form_valid(self, form):
        messages.success(self.request, _("Статус успешно обновлен"))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(
                request,
                _("Статус успешно удален"),
            )
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _("У вас нет прав для удаления этого статуса"),
            )
            return redirect("statuses:list")
