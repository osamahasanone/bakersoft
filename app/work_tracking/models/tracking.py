from django.conf import settings
from django.db import models

from work_tracking.models.state_machine import FiniteStateMachine


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = (
            "-created_at",
            "-updated_at",
        )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Team(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class JobTitle(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Employee(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Noqa E501
    job_title = models.ForeignKey(
        JobTitle, null=True, blank=True, on_delete=models.SET_NULL
    )
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    is_leader = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class Project(BaseModel, FiniteStateMachine):
    summary = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    manager = models.ForeignKey(Employee, on_delete=models.PROTECT)
    teams = models.ManyToManyField(to=Team)

    def __str__(self) -> str:
        return self.summary


class Task(BaseModel, FiniteStateMachine):
    summary = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    team_assigned_to = models.ForeignKey(Team, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    due_time = models.DateTimeField()

    def __str__(self) -> str:
        return self.summary


class WorkTimeLog(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    task = models.ForeignKey(
        Task, null=True, blank=True, on_delete=models.SET_NULL
    )  # Noqa E501
    since = models.DateTimeField()
    until = models.DateTimeField()
    achievement = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.achievment
