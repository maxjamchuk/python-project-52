from django import forms
from labels.models import Label
from .models import Task


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
