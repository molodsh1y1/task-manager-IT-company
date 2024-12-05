from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import (
    SignUpView,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView
)

app_name = "accounts"

urlpatterns = [
    path("register/", SignUpView.as_view(), name="sign_up"),
    path(
        "login/",
        LoginView.as_view(template_name="accounts/login.html"),
        name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout"
    ),
    path(
        "teams/",
        TeamListView.as_view(),
        name="team-list"
    ),
    path(
        "teams/<int:pk>/detail/",
        TeamDetailView.as_view(),
        name="team-detail"
    ),
    path(
        "teams/create/",
        TeamCreateView.as_view(),
        name="team-create"
    ),
    path(
        "teams/<int:pk>/update/",
        TeamUpdateView.as_view(),
        name="team-update"
    ),
    path(
        "teams/<int:pk>/delete/",
        TeamDeleteView.as_view(),
        name="team-delete"
    ),
]
