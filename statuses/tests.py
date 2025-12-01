from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Status

User = get_user_model()


class StatusCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user1",
            password="password123",
        )

    def setUp(self):
        self.client.login(username="user1", password="password123")

    def test_status_list_requires_login(self):
        self.client.logout()
        url = reverse("statuses:list")
        response = self.client.get(url)
        login_url = reverse("login")
        self.assertRedirects(response, f"{login_url}?next={url}")

    def test_status_create(self):
        url = reverse("statuses:create")
        data = {"name": "New"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(name="New").exists())

    def test_status_update(self):
        status = Status.objects.create(name="Old")
        url = reverse("statuses:update", args=[status.pk])
        data = {"name": "Updated"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("statuses:list"))

        status.refresh_from_db()
        self.assertEqual(status.name, "Updated")

    def test_status_delete(self):
        status = Status.objects.create(name="ToDelete")
        url = reverse("statuses:delete", args=[status.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())
