from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from .models import Task, Project
from .mixins import UserAssignedFormMixin
from .forms import (
    CreateTaskForm,
    TaskTitleSearchForm,
    ProjectNameSearchForm
)


class HomePageView(generic.TemplateView):
    template_name = "todo_list/index.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_queryset(self):
        title = self.request.GET.get("title")

        queryset = Task.objects.filter(
            Q(assignees=self.request.user) |
            Q(created_by=self.request.user) |
            Q(team__members=self.request.user)
        ).distinct()

        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = TaskTitleSearchForm(initial={"title": title})
        return context


class TaskDetailView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.DetailView
):
    model = Task

    def get_queryset(self):
        queryset = Task.objects.filter(
            Q(assignees=self.request.user) |
            Q(created_by=self.request.user) |
            Q(team__members=self.request.user)
        ).distinct()

        queryset = queryset.select_related("created_by")
        return queryset


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


class ToggleTaskStatusView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.View
):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get("name")

        queryset = Project.objects.filter(
            Q(team__members=self.request.user),
        ).distinct()

        queryset = queryset.select_related("team")

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = ProjectNameSearchForm(initial={"name": name})
        return context


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_queryset(self):
        title = self.request.GET.get("title")

        queryset = Project.objects.filter(
            team__members=self.request.user
        ).distinct()

        if title:
            queryset = queryset.filter(tasks__title__icontains=title)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(project=self.object)
        if tasks.exists():
            context["tasks"] = tasks

        title = self.request.GET.get("title", "")
        context["search_form"] = TaskTitleSearchForm(initial={"title": title})
        return context
