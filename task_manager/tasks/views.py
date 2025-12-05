from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = "tasks/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("status", "author", "executor")
            .prefetch_related("labels")
        )
        return qs


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        # автор — залогиненный пользователь
        form.instance.author = self.request.user
        messages.success(self.request, _("Задача успешно создана"))
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        messages.success(self.request, _("Задача успешно изменена"))
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(
                request,
                _("Задачу может удалить только ее автор"),
            )
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(
                request,
                _("Задачу может удалить только ее автор"),
            )
            return redirect(self.success_url)

        messages.success(
            request,
            _("Задача успешно удалена"),
        )
        return super().post(request, *args, **kwargs)

