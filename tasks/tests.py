from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from labels.models import Label
from statuses.models import Status
from .models import Task

User = get_user_model()


class TaskCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username="user1",
            password="password123",
        )
        cls.user2 = User.objects.create_user(
            username="user2",
            password="password123",
        )
        cls.status = Status.objects.create(name="New")

    def setUp(self):
        self.client.login(username="user1", password="password123")

    def test_task_list_requires_login(self):
        self.client.logout()
        url = reverse("tasks:list")
        response = self.client.get(url)
        login_url = reverse("login")
        self.assertRedirects(response, f"{login_url}?next={url}")

    def test_task_create(self):
        url = reverse("tasks:create")
        data = {
            "name": "Test task",
            "description": "Some description",
            "status": self.status.pk,
            "executor": self.user2.pk,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("tasks:list"))

        task = Task.objects.get(name="Test task")
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.status, self.status)

    def test_task_detail(self):
        task = Task.objects.create(
            name="Detail task",
            description="",
            status=self.status,
            author=self.user1,
        )
        url = reverse("tasks:detail", args=[task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail task")

    def test_task_update(self):
        task = Task.objects.create(
            name="Old name",
            description="Old desc",
            status=self.status,
            author=self.user1,
        )
        url = reverse("tasks:update", args=[task.pk])
        data = {
            "name": "Updated name",
            "description": "New desc",
            "status": self.status.pk,
            "executor": "",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("tasks:list"))

        task.refresh_from_db()
        self.assertEqual(task.name, "Updated name")
        self.assertEqual(task.description, "New desc")

    def test_task_delete_by_author(self):
        task = Task.objects.create(
            name="To delete",
            description="",
            status=self.status,
            author=self.user1,
        )
        url = reverse("tasks:delete", args=[task.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_task_delete_by_not_author_forbidden(self):
        task = Task.objects.create(
            name="Protected",
            description="",
            status=self.status,
            author=self.user1,
        )
        self.client.logout()
        self.client.login(username="user2", password="password123")

        url = reverse("tasks:delete", args=[task.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())

    def test_task_create_with_labels(self):
        label1 = Label.objects.create(name="bug")
        label2 = Label.objects.create(name="feature")

        url = reverse("tasks:create")
        data = {
            "name": "Task with labels",
            "description": "",
            "status": self.status.pk,
            "executor": self.user2.pk,
            "labels": [label1.pk, label2.pk],
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("tasks:list"))

        task = Task.objects.get(name="Task with labels")
        self.assertEqual(set(task.labels.all()), {label1, label2})
