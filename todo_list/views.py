from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from .models import Tag, Task, Project
from .forms import CreateTaskForm
from .mixins import UserAssignedFormMixin


class HomePageView(generic.TemplateView):
    template_name = "todo_list/index.html"


class TaskList(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(
            Q(assignees=self.request.user) |
            Q(created_by=self.request.user) |
            Q(team__members=self.request.user)
        ).distinct()


class TaskDetailView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.DetailView
):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(
            Q(assignees=self.request.user) |
            Q(created_by=self.request.user)
        )


class TaskCreateView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.CreateView
):
    form_class = CreateTaskForm
    template_name = "todo_list/task_form.html"
    success_url = reverse_lazy("todo:task-list")


class TaskUpdateView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.UpdateView
):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "todo_list/task_confirm_delete.html"
    success_url = reverse_lazy("todo:task-list")
