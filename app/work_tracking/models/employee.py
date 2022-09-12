from django.conf import settings
from django.db import models

from work_tracking.models.base import BaseModel


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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.ForeignKey(
        JobTitle, null=True, blank=True, on_delete=models.SET_NULL
    )
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    is_leader = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
