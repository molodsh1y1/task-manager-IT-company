from django.urls import path
from .views import (
    HomePageView,
    TaskList,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    ToggleTaskStatusView,
)


app_name = "todo"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("tasks/", TaskList.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/toggle-status/", ToggleTaskStatusView.as_view(), name="toggle-status"),
]
