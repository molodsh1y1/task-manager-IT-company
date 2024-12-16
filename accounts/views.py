from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from todo_list.models import Project
from accounts.models import Team, TeamMembership
from accounts.forms import (
    RegisterForm,
    TeamCreateForm,
    TeamNameSearchForm
)


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
        queryset = Team.objects.filter(
            Q(members=self.request.user) |
            Q(created_by=self.request.user)
        ).prefetch_related("members")

        name = self.request.GET.get("name", "")

        if name:
            queryset = queryset.filter(name__icontains=name)

        queryset = queryset.select_related("created_by")

        queryset = queryset.order_by("name")

        return queryset.distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TeamNameSearchForm(
            initial={"name": name}
        )
        return context


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    template_name = "accounts/team_detail.html"
    context_object_name = "team"
    paginate_by = 10

    def get_queryset(self):
        return Team.objects.select_related("created_by")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object

        if self.request.user in team.members.all():
            context["projects"] = Project.objects.filter(
                team=team
            ).select_related("team", "created_by")
        else:
            context["projects"] = Project.objects.none()

        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy("accounts:team-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["current_user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        members = form.cleaned_data.pop("members", [])
        team = form.save()

        TeamMembership.objects.create(
            team=team,
            worker=self.request.user,
            role=self.request.user.position,
            joined_at=datetime.now(),
            is_active=True
        )

        for member in members:
            TeamMembership.objects.create(
                team=team,
                worker=member,
                role=member.position,
                joined_at=datetime.now(),
                is_active=True
            )

        return super().form_valid(form)


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy("accounts:team-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["current_user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        team = form.save()

        new_members = list(form.cleaned_data["members"])

        if team.created_by not in new_members:
            new_members.append(team.created_by)

        existing_members = set(team.members.all())

        for member in new_members:
            if member not in existing_members:
                TeamMembership.objects.get_or_create(
                    team=team,
                    worker=member,
                )

        for member in existing_members:
            if member not in new_members:
                TeamMembership.objects.filter(
                    team=team,
                    worker=member
                ).delete()

        return super().form_valid(form)


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("accounts:team-list")
