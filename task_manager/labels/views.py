from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/list.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ("name",)
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        messages.success(self.request, _("Label has been created successfully"))
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ("name",)
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        messages.success(self.request, _("Label has been updated successfully"))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(
                request,
                _("It is not possible to delete a label because it is in use"),
            )
            return redirect("labels:list")

        messages.success(
            request,
            _("Label has been deleted successfully"),
        )
        return super().post(request, *args, **kwargs)


