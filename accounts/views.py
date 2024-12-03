from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from todo_list.forms import TaskTitleSearchForm
from .forms import RegisterForm
from .models import Team, TeamMembership
from todo_list.models import Task


class SignUpView(generic.FormView):
    form_class = RegisterForm
    success_url = reverse_lazy("todo:home")
    template_name = "accounts/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    template_name = "accounts/team_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Team.objects.filter(
            members=self.request.user
        ).prefetch_related('members')


class TeamTaskDetailView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "accounts/team_detail.html"
    context_object_name = "tasks"

    def get_queryset(self):
        team = get_object_or_404(Team, pk=self.kwargs["pk"])

        if not team.members.filter(pk=self.request.user.pk).exists():
            raise PermissionError("You are not a member of this team")

        title = self.request.GET.get("title")

        if title:
            return Task.objects.filter(team=team, title__icontains=title)

        return Task.objects.filter(team=team)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = TaskTitleSearchForm(initial={"title": title})
        return context
