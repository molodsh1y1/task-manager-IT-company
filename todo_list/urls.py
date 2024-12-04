from django.urls import path
from .views import (
    HomePageView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    ToggleTaskStatusView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
)


app_name = "todo"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/toggle-status/",
        ToggleTaskStatusView.as_view(),
        name="toggle-status"
    ),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="project-create"
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
]
