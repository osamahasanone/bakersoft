import pytest
from model_bakery import baker

from work_tracking.models import Employee, Task, WorkTimeLog

pytestmark = pytest.mark.django_db


def test_employee_see_his_logs(api_client, employee):
    # invlove employee team in a project
    task = baker.make(Task, team_assigned_to=employee.team)
    # employee added logs
    baker.make(WorkTimeLog, employee=employee, task=task)
    baker.make(WorkTimeLog, employee=employee, task=task)

    # invlove employee team in another project
    another_task = baker.make(Task, team_assigned_to=employee.team)
    # employee added logs
    baker.make(WorkTimeLog, employee=employee, task=another_task)

    # Action
    response = api_client.get("/tracking/logs/")

    # Assert
    assert len(response.json()) == 3
    assert response.status_code == 200


def test_employee_see_others_logs_on_project_his_team_ivolved_in(api_client, employee):
    # invlove employee team in a project
    task = baker.make(Task, team_assigned_to=employee.team)
    # employee added logs
    baker.make(WorkTimeLog, employee=employee, task=task)
    baker.make(WorkTimeLog, employee=employee, task=task)
    # teamate added logs
    teammate = baker.make(Employee, team=employee.team)
    baker.make(WorkTimeLog, employee=teammate, task=task)
    # another team member added logs
    another_team_member = baker.make(Employee)
    baker.make(WorkTimeLog, employee=another_team_member, task=task)

    # Action
    response = api_client.get("/tracking/logs/")

    # Assert
    assert len(response.json()) == 4
    assert response.status_code == 200


def test_employee_cant_see_logs_on_project_his_team_not_ivolved_in(
    api_client, employee
):
    another_team_member = baker.make(Employee)
    # invlove other team in a project
    task = baker.make(Task, team_assigned_to=another_team_member.team)
    # new logs to the project
    baker.make(WorkTimeLog, employee=another_team_member, task=task)
    baker.make(WorkTimeLog, employee=another_team_member, task=task)

    # Action
    response = api_client.get("/tracking/logs/")

    # Assert
    assert len(response.json()) == 0
    assert response.status_code == 200


def test_employee_see_his_log_entry(api_client, employee):
    # Arrange
    task = baker.make(Task, team_assigned_to=employee.team)
    log_entry = baker.make(WorkTimeLog, employee=employee, task=task)

    # Action
    response = api_client.get(f"/tracking/logs/{log_entry.id}/")

    # Assert
    assert response.json() == {
        "id": log_entry.id,
        "employee": employee.id,
        "task": task.id,
        "project": task.project.id,
        "since": log_entry.since.strftime("%Y-%m-%dT%H:%M:%S"),
        "until": log_entry.until.strftime("%Y-%m-%dT%H:%M:%S"),
        "achievement": log_entry.achievement,
        "details": log_entry.details,
        "created_at": log_entry.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    assert response.status_code == 200


def test_employee_see_other_employee_log_entry(api_client, employee):
    # Arrange
    task = baker.make(Task, team_assigned_to=employee.team)
    # teamate added logs
    teammate = baker.make(Employee, team=employee.team)
    log_entry = baker.make(WorkTimeLog, employee=teammate, task=task)

    # Action
    response = api_client.get(f"/tracking/logs/{log_entry.id}/")

    # Assert
    assert response.json() == {
        "id": log_entry.id,
        "employee": teammate.id,
        "task": task.id,
        "project": task.project.id,
        "since": log_entry.since.strftime("%Y-%m-%dT%H:%M:%S"),
        "until": log_entry.until.strftime("%Y-%m-%dT%H:%M:%S"),
        "achievement": log_entry.achievement,
        "details": log_entry.details,
        "created_at": log_entry.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    assert response.status_code == 200


def test_employee_cant_see_log_entry_of_project_his_team_not_envolved_in(api_client):
    another_team_member = baker.make(Employee)
    task = baker.make(Task, team_assigned_to=another_team_member.team)
    log_entry = baker.make(WorkTimeLog, employee=another_team_member, task=task)

    # Action
    response = api_client.get(f"/tracking/logs/{log_entry.id}/")

    # Assert
    assert response.status_code == 404


def test_employee_modify_his_log_entry(api_client, employee):
    # Arrange
    task = baker.make(Task, team_assigned_to=employee.team)
    log_entry = baker.make(WorkTimeLog, employee=employee, task=task)
    new_summary = "new summary"

    # Action
    response = api_client.put(
        f"/tracking/logs/{log_entry.id}/",
        {
            "task": task.id,
            "since": "2022-09-12T13:00:00",
            "until": "2022-09-12T15:00:00",
            "achievement": new_summary,
            "details": "any",
        },
        format="json",
    )

    # Assert
    assert response.status_code == 200
    log_entry.refresh_from_db()
    assert log_entry.achievement == new_summary


def test_employee_cant_modify_other_log_entry(api_client):
    # Arrange
    another_team_member = baker.make(Employee)
    task = baker.make(Task, team_assigned_to=another_team_member.team)
    log_entry = baker.make(WorkTimeLog, employee=another_team_member, task=task)
    new_summary = "new summary"

    # Action
    response = api_client.put(
        f"/tracking/logs/{log_entry.id}/",
        {
            "task": task.id,
            "since": "2022-09-12T13:00:00",
            "until": "2022-09-12T15:00:00",
            "achievement": new_summary,
            "details": "any",
        },
        format="json",
    )

    # Assert
    assert response.status_code == 404


def test_employee_delete_his_log_entry(api_client, employee):
    # Arrange
    task = baker.make(Task, team_assigned_to=employee.team)
    log_entry = baker.make(WorkTimeLog, employee=employee, task=task)

    # Action
    response = api_client.delete(f"/tracking/logs/{log_entry.id}/")

    # Assert
    assert response.status_code == 204
    assert WorkTimeLog.objects.count() == 0


def test_employee_cant_delete_other_log_entry(api_client):
    # Arrange
    another_team_member = baker.make(Employee)
    task = baker.make(Task, team_assigned_to=another_team_member.team)
    log_entry = baker.make(WorkTimeLog, employee=another_team_member, task=task)

    # Action
    response = api_client.delete(f"/tracking/logs/{log_entry.id}/")

    # Assert
    assert response.status_code == 404
