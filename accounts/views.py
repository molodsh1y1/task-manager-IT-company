from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import RegisterForm
from .models import Team
from todo_list.models import Project


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
            Q(members=self.request.user) |
            Q(owner=self.request.user)
        ).prefetch_related('members')


class TeamDetailView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = "accounts/team_detail.html"
    context_object_name = "projects"

    def get_queryset(self):
        self.team = get_object_or_404(Team, pk=self.kwargs["pk"])

        if self.request.user in self.team.members.all():
            return Project.objects.filter(
                team=self.team
            ).select_related("team")
        return Project.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.team
        return context
