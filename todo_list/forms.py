from django import forms

from todo_list.models import Task, Team, Project


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "deadline",
            "priority",
            "task_type",
            "tags",
            "is_completed",
            "project",
            "team",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Task description"
                }
            ),
            "deadline": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            "is_completed": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
            "project": forms.Select(attrs={"class": "form-select"}),
            "team": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["team"].queryset = Team.objects.filter(members=user)
        self.fields["project"].queryset = Project.objects.filter(
            team__members=user
        )


class TaskTitleSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by task title"
            }
        ),
    )


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "status", "team"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter project name"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Project description"
                }
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "team": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["team"].queryset = Team.objects.filter(members=user)


class ProjectNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by project name"
            }
        ),
    )
