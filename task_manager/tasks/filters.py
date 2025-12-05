import django_filters
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Статус"),
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Исполнитель"),
    )

    label = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label=_("Метка"),
    )

    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
        label=_("Только свои задачи"),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label", "self_tasks"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        executor_field = self.form.fields.get("executor")
        if executor_field is not None:
            executor_field.label_from_instance = (
                lambda user: f"{user.first_name} {user.last_name}".strip()
            )

    def filter_self_tasks(self, queryset, name, value):
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
