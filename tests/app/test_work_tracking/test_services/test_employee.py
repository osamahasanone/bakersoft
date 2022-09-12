import pytest
from model_bakery import baker

from work_tracking.models import Employee, Task, Team
from work_tracking.services.employee import can_add_log

pytestmark = pytest.mark.django_db


def test_can_add_log_when_no_task():
    emp = baker.make(Employee)
    assert can_add_log(employee=emp, task=None)


def test_can_add_log_when_task_assigned_to_employee_team():
    team = baker.make(Team)
    emp = baker.make(Employee, team=team)
    task = baker.make(Task, team_assigned_to=team)
    assert can_add_log(emp, task)


def test_can_not_add_log_when_task_assigned_to_another_team():
    emp = baker.make(Employee)
    another_team = baker.make(Team)
    task = baker.make(Task, team_assigned_to=another_team)
    assert not can_add_log(emp, task)
