from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First Name"
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last Name"
    )
    email = forms.CharField(
        max_length=30,
        required=True,
        label="Email"
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "username",
            "email", "password1", "password2",
        )
