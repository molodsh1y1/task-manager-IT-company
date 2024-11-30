from django.contrib.auth import get_user_model
from django.db import models
from accounts.models import Team


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Status(models.TextChoices):
    """Choices for the status of a project."""
    NOT_STARTED = 'NOT_STARTED', 'Not Started'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    BLOCKED = 'BLOCKED', 'Blocked'


class TaskType(models.TextChoices):
    """Choices for the type of task."""
    BUG = "BUG", "Bug"
    NEW_FEATURE = "NEW_FEATURE", "New Feature"
    BREAKING_CHANGE = "BREAKING_CHANGE", "Breaking Change"
    REFACTORING = "REFACTORING", "Refactoring"
    QA = "QA", "Quality Assurance"


class Priority(models.TextChoices):
    """Choices for task priority"""
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.NEW_FEATURE,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    assignees = models.ManyToManyField(
        get_user_model(),
        related_name="tasks",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="tasks",
    )

    def __str__(self):
        return self.title
