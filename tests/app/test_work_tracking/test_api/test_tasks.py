import pytest
from model_bakery import baker

from work_tracking.models import Project, Task, TaskStateChange
from work_tracking.models.state_machine import State as TaskState

pytestmark = pytest.mark.django_db


def test_transition_task_by_team_leader(api_client, employee):
    # Arrange
    task = baker.make(Task, team_assigned_to=employee.team)
    employee.is_leader = True
    employee.save()

    # Action
    response = api_client.post(
        f"/tracking/tasks/{task.id}/transition/",
        {
            "state": TaskState.IN_PROGRESS,
            "comment": "any",
            "transitioned_at": "2022-09-12T17:05:00",
        },
        format="json",
    )

    # Assert
    assert response.status_code == 200
    task.refresh_from_db()
    assert task.state == TaskState.IN_PROGRESS
    assert TaskStateChange.objects.count() == 1


def test_transition_task_returns_bad_request_when_state_not_allowed(
    api_client, employee
):
    # Arrange
    task = baker.make(Task, team_assigned_to=employee.team)
    employee.is_leader = True
    employee.save()

    # Action
    response = api_client.post(
        f"/tracking/tasks/{task.id}/transition/",
        {
            "state": TaskState.COMPLETED,
            "comment": "any",
            "transitioned_at": "2022-09-12T17:05:00",
        },
        format="json",
    )

    # Assert
    assert response.json() == {
        "error": {
            "status_code": 400,
            "message": "Bad request syntax or unsupported method",
            "details": {"detail": "State change violates the rules"},
        }
    }


def test_transition_task_returns_unauthorized_when_team_member(api_client, employee):
    # Arrange
    task = baker.make(Task, team_assigned_to=employee.team)

    # Action
    response = api_client.post(
        f"/tracking/tasks/{task.id}/transition/",
        {
            "state": TaskState.IN_PROGRESS,
            "comment": "any",
            "transitioned_at": "2022-09-12T17:05:00",
        },
        format="json",
    )

    # Assert
    assert response.status_code == 403


def test_add_task_returns_when_due_after_start_time(api_client, employee):
    # Arrange
    project = baker.make(Project)

    # Action
    response = api_client.post(
        "/tracking/tasks/",
        {
            "summary": "any",
            "description": "any",
            "project": project.id,
            "team_assigned_to": employee.team.id,
            "start_time": "2022-09-10T15:00:00",
            "due_time": "2022-09-09T15:00:00",
        },
        format="json",
    )

    # Assert
    assert response.json() == {
        "error": {
            "status_code": 400,
            "message": "Bad request syntax or unsupported method",
            "details": {"non_field_errors": ["Due time should be after start time"]},
        }
    }
