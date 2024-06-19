from django.contrib import admin

from project_management.project.models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    search_fields = (
        'name',
        'description',
    )


# Task admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status',
        'due_date',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'status',
        'due_date',
    )
