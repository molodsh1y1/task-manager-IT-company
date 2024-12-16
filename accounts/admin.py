from django.contrib import admin

from accounts.models import (
    Worker,
    Team,
    TeamMembership
)


class WorkerAdmin(admin.ModelAdmin):
    list_display = ("username", "position", "email", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")


class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ("worker", "team", "role", "joined_at", "is_active")
    search_fields = ("worker__username", "team__name")


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Team)
admin.site.register(TeamMembership, TeamMembershipAdmin)
