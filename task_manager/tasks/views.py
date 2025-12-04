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


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Task has been created successfully"))
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        messages.success(self.request, _("Task has been updated successfully"))
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(
                request,
                _("You have no rights to delete this task"),
            )
            return redirect("tasks:list")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Task has been deleted successfully"))
        return super().delete(request, *args, **kwargs)



class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("status", "author", "executor")
            .prefetch_related("labels")
        )
        return qs
