from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Team
from todo_list.models import Task


class SignUpViewTests(TestCase):
    def setUp(self):
        self.signup_url = reverse("accounts:sign_up")
        self.valid_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password1": "SecurePassword123",
            "password2": "SecurePassword123",
        }
        self.invalid_data = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "not-an-email",
            "password1": "short",
            "password2": "mismatch",
        }

    def test_signup_view_renders_correct_template(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_signup_with_valid_data_creates_user(self):
        response = self.client.post(self.signup_url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(username="testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "johndoe@example.com")

    def test_signup_with_invalid_data_does_not_create_user(self):
        response = self.client.post(self.signup_url, self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username="").exists())


class TeamListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="password123"
        )
        self.team = Team.objects.create(name="Test Team")
        self.team.members.add(self.user)
        self.task = Task.objects.create(
            team=self.team,
            title="Test Task",
            description="Test Description",
            is_completed=False,
            created_by=self.user
        )
        self.url = reverse("accounts:team-list")

    def test_team_task_detail_requires_login(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_team_list_view_shows_teams(self):
        self.client.login(username="tester", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/team_list.html")
        self.assertContains(response, "Test Team")
