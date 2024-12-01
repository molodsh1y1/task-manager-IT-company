from django.urls import path
from .views import (
    SignUpView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", SignUpView.as_view(), name="sign_up")
]

