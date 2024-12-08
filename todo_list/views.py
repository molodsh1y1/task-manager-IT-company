from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from accounts.models import Team
from .models import Task, Project
from .mixins import UserAssignedFormMixin
from .forms import (
    TaskCreateForm,
    TaskTitleSearchForm,
    ProjectNameSearchForm,
    ProjectCreateForm
)


class HomePageView(generic.TemplateView):
    template_name = "todo_list/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["task_num"] = Task.objects.count()
        context["project_num"] = Project.objects.count()
        context["team_num"] = Team.objects.count()

        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get("task_id")
        if task_id:
            task = get_object_or_404(Task, pk=task_id)
            task.is_completed = not task.is_completed
            task.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = TaskTitleSearchForm(initial={"title": title})
        return context


class TaskDetailView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.DetailView
):
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
    form_class = TaskCreateForm
    template_name = "todo_list/task_form.html"
    success_url = reverse_lazy("todo:task-list")


class TaskUpdateView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.UpdateView
):
    form_class = TaskCreateForm
    success_url = reverse_lazy("todo:task-list")

    def get_queryset(self):
        queryset = Task.objects.filter(
            Q(assignees=self.request.user) |
            Q(created_by=self.request.user) |
            Q(team__members=self.request.user)
        ).distinct()

        queryset = queryset.select_related("created_by")
        return queryset


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "todo_list/task_confirm_delete.html"
    success_url = reverse_lazy("todo:task-list")


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get("name")

        queryset = Project.objects.filter(
            Q(team__members=self.request.user) |
            Q(created_by=self.request.user)
        ).prefetch_related("created_by").distinct()

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
            Q(team__members=self.request.user) |
            Q(created_by=self.request.user)
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


class ProjectUpdateView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.UpdateView
):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy("todo:project-list")


class ProjectCreateView(
    LoginRequiredMixin,
    UserAssignedFormMixin,
    generic.CreateView
):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy("todo:project-list")


class ProjectDeleteView(
    LoginRequiredMixin,
    generic.DeleteView
):
    model = Project
    success_url = reverse_lazy("todo:project-list")
