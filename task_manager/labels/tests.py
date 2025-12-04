from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status

User = get_user_model()


class LabelCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user1",
            password="password123",
        )
        cls.status = Status.objects.create(name="New")

    def setUp(self):
        self.client.login(username="user1", password="password123")

    def test_label_list_requires_login(self):
        self.client.logout()
        url = reverse("labels:list")
        response = self.client.get(url)
        login_url = reverse("login")
        self.assertRedirects(response, f"{login_url}?next={url}")

    def test_label_create(self):
        url = reverse("labels:create")
        data = {"name": "bug"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("labels:list"))
        self.assertTrue(Label.objects.filter(name="bug").exists())

    def test_label_update(self):
        label = Label.objects.create(name="old")
        url = reverse("labels:update", args=[label.pk])
        data = {"name": "new"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("labels:list"))

        label.refresh_from_db()
        self.assertEqual(label.name, "new")

    def test_label_delete_without_tasks(self):
        label = Label.objects.create(name="temp")
        url = reverse("labels:delete", args=[label.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("labels:list"))
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())

    def test_label_delete_with_tasks_forbidden(self):
        label = Label.objects.create(name="important")
        task = Task.objects.create(
            name="Test task",
            description="",
            status=self.status,
            author=self.user,
        )
        task.labels.add(label)

        url = reverse("labels:delete", args=[label.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("labels:list"))
        self.assertTrue(Label.objects.filter(pk=label.pk).exists())
