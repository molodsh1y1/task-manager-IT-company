from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.TextChoices):
    DEVELOPER = "DEVELOPER", "Developer"
    MANAGER = "MANAGER", "Project Manager"
    QA = "QA", "Quality assurance"
    DESIGNER = "DESIGNER", "Designer"
    DEVOPS = "DEVOPS", "DevOps"


class Worker(AbstractUser):
    email = models.EmailField(unique=True)
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.DEVELOPER,
    )

    def __str__(self):
        return f"{self.username} - {self.get_position_display()}"


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(
        Worker,
        related_name="teams",
        through="TeamMembership"
    )
    created_by = models.ForeignKey(
        Worker,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_teams"
    )

    def get_member_count(self) -> int:
        return self.members.count()

    def __str__(self) -> str:
        return self.name


class TeamMembership(models.Model):
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name="team_memberships"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="team_memberships"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (
            f"{self.worker} in {self.team}, as "
            f"{self.role if self.role else 'member'}"
        )
