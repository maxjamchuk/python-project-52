from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserCrudTests(TestCase):
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

    def test_user_list_page(self):
        url = reverse("users:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_user_create(self):
        url = reverse("users:create")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "newuser",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_update_self(self):
        self.client.login(username="user1", password="password123")
        url = reverse("users:update", args=[self.user1.pk])
        data = {
            "username": "user1",
            "first_name": "John",
            "last_name": "Doe",
            "email": self.user1.email,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("users:list"))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "John")

    def test_user_update_other_forbidden(self):
        self.client.login(username="user1", password="password123")
        url = reverse("users:update", args=[self.user2.pk])
        response = self.client.post(url, {})
        self.assertRedirects(response, reverse("users:list"))

    def test_user_delete_self(self):
        self.client.login(username="user1", password="password123")
        url = reverse("users:delete", args=[self.user1.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("users:list"))
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())

    def test_user_delete_other_forbidden(self):
        self.client.login(username="user1", password="password123")
        url = reverse("users:delete", args=[self.user2.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("users:list"))
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())

    def test_login_redirects_to_index(self):
        url = reverse("login")
        response = self.client.post(
            url,
            {"username": "user1", "password": "password123"},
        )
        self.assertRedirects(response, reverse("index"))
