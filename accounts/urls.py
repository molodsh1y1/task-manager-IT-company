from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import (
    SignUpView,
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
]

