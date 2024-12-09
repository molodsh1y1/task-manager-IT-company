from django.test import TestCase
from django.urls import reverse

from accounts.models import (
    Team,
    Position,
    Worker,
)


class SignUpViewTests(TestCase):
    def setUp(self) -> None:
        self.signup_url = reverse("accounts:sign_up")
        self.valid_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "position": Position.DEVELOPER,
            "password1": "SecurePassword123",
            "password2": "SecurePassword123",
        }
        self.invalid_data = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "not-an-email",
            "position": "cooker",
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
        user = Worker.objects.get(username="testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "johndoe@example.com")

    def test_signup_with_invalid_data_does_not_create_user(self):
        response = self.client.post(self.signup_url, self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Worker.objects.filter(username="").exists())


class TeamListViewTests(TestCase):
    def setUp(self):
        self.user = Worker.objects.create_user(
            username="testuser", password="password123"
        )
        self.team = Team.objects.create(name="Test Team", created_by=self.user)
        self.url = reverse('accounts:team-list')

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_team_list_view_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")

    def test_search_functionality(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url, {'name': 'Test'})
        self.assertContains(response, "Test Team")
        self.assertEqual(len(response.context['object_list']), 1)


class TeamDetailViewTests(TestCase):
    def setUp(self):
        self.user = Worker.objects.create_user(
            username="testuser", password="password123"
        )
        self.team = Team.objects.create(name="Test Team", created_by=self.user)

        self.url = reverse("accounts:team-detail", kwargs={"pk": self.team.pk})

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_team_detail_view_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")

    def test_team_member_access(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")


class TeamCreateViewTests(TestCase):
    def setUp(self):
        self.user = Worker.objects.create_user(
            username="testuser", password="password123"
        )
        self.url = reverse("accounts:team-create")

    def test_create_team_view_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {"name": "New Team", "created_by": self.user}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("accounts:team-list"))
        self.assertEqual(Team.objects.count(), 1)

    def test_create_team_view_not_authenticated(self):
        response = self.client.post(self.url, {"name": "New Team"})
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')


class TeamUpdateViewTests(TestCase):
    def setUp(self):
        self.user = Worker.objects.create_user(
            username="testuser", password="password123"
        )
        self.team = Team.objects.create(name="Test Team", created_by=self.user)
        self.url = reverse("accounts:team-update", kwargs={"pk": self.team.pk})

    def test_update_team_view_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {"name": "Updated Team", "created_by": self.user.id}
        response = self.client.post(self.url, data)
        self.team.refresh_from_db()
        self.assertRedirects(response, reverse("accounts:team-list"))
        self.assertEqual(self.team.name, "Updated Team")

    def test_update_team_view_not_authenticated(self):
        response = self.client.post(self.url, {"name": "Updated Team"})
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')


class TeamDeleteViewTests(TestCase):
    def setUp(self):
        self.user = Worker.objects.create_user(
            username="testuser", password="password123"
        )
        self.team = Team.objects.create(name="Test Team", created_by=self.user)
        self.url = reverse("accounts:team-delete", kwargs={"pk": self.team.pk})

    def test_delete_team_view_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("accounts:team-list"))
        self.assertEqual(Team.objects.count(), 0)

    def test_delete_team_view_not_authenticated(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
