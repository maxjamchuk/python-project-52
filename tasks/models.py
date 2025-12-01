from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name=_("Status"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        verbose_name=_("Author"),
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="executed_tasks",
        null=True,
        blank=True,
        verbose_name=_("Executor"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name="tasks",
        verbose_name=_("Labels"),
    )

    def __str__(self) -> str:
        return self.name
