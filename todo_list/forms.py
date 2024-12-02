from django import forms

from .models import Task, Team


class CreateTaskForm(forms.ModelForm):
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
            "team",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter task title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Task description"}),
            "deadline": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "team": forms.Select(attrs={"class": "form-select"}),
        }
