from django.contrib import admin

from work_tracking.models import (
    Employee,
    JobTitle,
    Project,
    Task,
    TaskStateChange,
    Team,
    WorkTimeLog,
)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskStateChange)
class TaskStateChangeAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkTimeLog)
class WorkTimeLogAdmin(admin.ModelAdmin):
    pass
