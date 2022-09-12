import arrow
import pytest
from model_bakery import baker

from work_tracking.models import Employee, Project, Task, Team, WorkTimeLog
from work_tracking.services.project import (
    get_active_employees,
    get_assigned_to_teams,
    get_estimated_hours,
)

pytestmark = pytest.mark.django_db


def test_get_estimated_hours_when_tasks_existed():
    project = baker.make(Project)
    now = arrow.utcnow()
    # project starts after (2) hour
    baker.make(
        Task,
        project=project,
        start_time=now.shift(hours=2).datetime,
        due_time=now.shift(hours=4).datetime,
    )
    baker.make(
        Task,
        project=project,
        start_time=now.shift(hours=12).datetime,
        due_time=now.shift(hours=14).datetime,
    )
    # project is due after (24) hour
    baker.make(
        Task,
        project=project,
        start_time=now.shift(hours=22).datetime,
        due_time=now.shift(hours=24).datetime,
    )
    assert get_estimated_hours(project) == 22.0


def test_get_estimated_hours_when_tasks_not_existed():
    project = baker.make(Project)
    assert get_estimated_hours(project) is None


def test_get_assigned_to_teams():
    project = baker.make(Project)
    team_1 = baker.make(Team)
    team_2 = baker.make(Team)
    team_3 = baker.make(Team)
    baker.make(Task, project=project, team=team_1)
    baker.make(Task, project=project, team=team_2)
    baker.make(Task, project=project, team=team_3)
    assert get_assigned_to_teams(project) == 3


def test_get_active_to_employees():
    project = baker.make(Project)
    task_1 = baker.make(Task, project=project)
    task_2 = baker.make(Task, project=project)
    emp_1 = baker.make(Employee)
    emp_2 = baker.make(Employee)
    baker.make(WorkTimeLog, task=task_1, employee=emp_1)
    baker.make(WorkTimeLog, task=task_1, employee=emp_1)
    baker.make(WorkTimeLog, task=task_2, employee=emp_2)
    assert get_active_employees(project) == 2
