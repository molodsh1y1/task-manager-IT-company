from django.test import TestCase
from accounts.models import (
    Worker,
    Team,
    TeamMembership,
    Position,
)


class WorkerModelTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create(
            username="john_doe",
            email="john.doe@example.com",
            password="securepassword",
            position=Position.MANAGER,
        )

    def test_worker_creation(self):
        self.assertEqual(Worker.objects.count(), 1)
        self.assertEqual(self.worker.username, "john_doe")
        self.assertEqual(self.worker.email, "john.doe@example.com"),
        self.assertEqual(self.worker.position, Position.MANAGER)
        self.assertEqual(self.worker.get_position_display(), "Project Manager")

    def test_worker_string_representation(self):
        self.assertEqual(str(self.worker), "john_doe - Project Manager")


class TeamModelTest(TestCase):
    def setUp(self):
        self.created_by = Worker.objects.create(
            username="john_doe",
            email="john.doe@example.com",
            password="securepassword",
            position=Position.MANAGER,
        )
        self.team = Team.objects.create(
            name="Team Alpha",
            created_by=self.created_by
        )

    def test_team_creation(self):
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(self.team.name, "Team Alpha")
        self.assertEqual(self.team.created_by, self.created_by)

    def test_team_string_representation(self):
        self.assertEqual(str(self.team), "Team Alpha")

    def test_team_member_count(self):
        self.assertEqual(self.team.get_member_count(), 0)

        worker = Worker.objects.create_user(
            username="member_user",
            email="member@example.com",
            password="securepassword",
            position=Position.QA,
        )
        TeamMembership.objects.create(worker=worker, team=self.team)
        self.assertEqual(self.team.get_member_count(), 1)


class TeamMembershipModelTest(TestCase):
    def setUp(self):
        self.created_by = Worker.objects.create(
            username="john_doe",
            email="john.doe@example.com",
            password="securepassword",
            position=Position.MANAGER,
        )
        self.team = Team.objects.create(
            name="Team Alpha",
            created_by=self.created_by
        )
        self.membership = TeamMembership.objects.create(
            worker=self.created_by,
            team=self.team,
            role="created_by",
        )

    def test_team_membership_creation(self):
        self.assertEqual(TeamMembership.objects.count(), 1)
        self.assertEqual(self.membership.worker, self.created_by)
        self.assertEqual(self.membership.team, self.team)
        self.assertEqual(self.membership.role, "created_by")
        self.assertTrue(self.membership.is_active)

    def test_team_membership_string_representation(self):
        self.assertEqual(
            str(self.membership),
            "john_doe - Project Manager in Team Alpha, as created_by",
        )
