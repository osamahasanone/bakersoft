import arrow
import pytest
from model_bakery import baker

from work_tracking.models import Employee, Project, Task, Team, WorkTimeLog

pytestmark = pytest.mark.django_db


def test_get_stats(api_client, employee):
    # Arrange
    project = baker.make(Project)
    another_team = baker.make(Team)

    now = arrow.utcnow()
    task_1 = baker.make(
        Task,
        project=project,
        team_assigned_to=employee.team,
        start_time=now.shift(hours=2).datetime,
        due_time=now.shift(hours=4).datetime,
    )
    task_2 = baker.make(
        Task,
        project=project,
        team_assigned_to=another_team,
        start_time=now.shift(hours=12).datetime,
        due_time=now.shift(hours=14).datetime,
    )
    task_3 = baker.make(
        Task,
        project=project,
        team_assigned_to=another_team,
        start_time=now.shift(hours=22).datetime,
        due_time=now.shift(hours=24).datetime,
    )

    another_employee = baker.make(Employee, team=another_team)
    baker.make(WorkTimeLog, task=task_1, employee=another_employee)
    baker.make(WorkTimeLog, task=task_2, employee=another_employee)
    baker.make(WorkTimeLog, task=task_3, employee=another_employee)

    # Action
    response = api_client.get(f"/tracking/projects/{project.id}/stats/")

    # Assert
    assert response.json() == {
        "estimated_hours": 22.0,
        "teams": 2,
        "active_employees": 1,
    }
    assert response.status_code == 200
