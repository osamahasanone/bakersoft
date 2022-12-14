from django.db import models

from work_tracking.models.base import BaseModel
from work_tracking.models.employee import Employee, Team
from work_tracking.models.state_machine import FiniteStateMachine, State


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
    start_time = models.DateTimeField(db_index=True)
    due_time = models.DateTimeField(db_index=True)

    def __str__(self) -> str:
        return self.summary


class TaskStateChange(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    state = models.CharField(choices=State.choices, max_length=255)
    comment = models.CharField(max_length=255)
    transitioned_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.task} - {self.state}"


class WorkTimeLog(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL)
    since = models.DateTimeField()
    until = models.DateTimeField()
    achievement = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.achievement
