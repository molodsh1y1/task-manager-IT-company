from django.contrib import admin

from todo_list.models import Task, Project, Tag


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "is_completed", "deadline", "team")
    search_fields = ("title", "description")
    list_filter = ("priority", "status", "task_type")


admin.site.register(Task, TaskAdmin)
admin.site.register(Project)
admin.site.register(Tag)
