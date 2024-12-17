from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Team


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
            "email", "position", "password1",
            "password2",
        )


class TeamCreateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label="Members",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Team
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter team name"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)

        if current_user:
            self.fields["members"].queryset = get_user_model().objects.exclude(
                pk=current_user.pk
            )


class TeamNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by team name"
            }
        ),
    )
