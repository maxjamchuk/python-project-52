from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import LabelForm
from .models import Label
from task_manager.tasks.models import Task


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно создана"))
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно изменена"))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if Task.objects.filter(labels=self.object).exists():
            messages.error(
                request,
                _("Невозможно удалить метку"),
            )
            return redirect(self.success_url)

        messages.success(
            request,
            _("Метка успешно удалена"),
        )
        return super().post(request, *args, **kwargs)
