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
        self.owner = Worker.objects.create(
            username="john_doe",
            email="john.doe@example.com",
            password="securepassword",
            position=Position.MANAGER,
        )
        self.team = Team.objects.create(name="Team Alpha", owner=self.owner)

    def test_team_creation(self):
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(self.team.name, "Team Alpha")
        self.assertEqual(self.team.owner, self.owner)

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
        self.owner = Worker.objects.create(
            username="john_doe",
            email="john.doe@example.com",
            password="securepassword",
            position=Position.MANAGER,
        )
        self.team = Team.objects.create(name="Team Alpha", owner=self.owner)
        self.membership = TeamMembership.objects.create(
            worker=self.owner,
            team=self.team,
            role="Owner",
        )

    def test_team_membership_creation(self):
        self.assertEqual(TeamMembership.objects.count(), 1)
        self.assertEqual(self.membership.worker, self.owner)
        self.assertEqual(self.membership.team, self.team)
        self.assertEqual(self.membership.role, "Owner")
        self.assertTrue(self.membership.is_active)

    def test_team_membership_string_representation(self):
        self.assertEqual(
            str(self.membership),
            "john_doe - Project Manager in Team Alpha, as Owner",
        )
