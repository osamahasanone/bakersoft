import logging

import arrow
import pytest
from model_bakery import baker

from work_tracking.models import Employee, Task, Team
from work_tracking.tasks import notify_team_leaders_about_tasks_overdue_soon

pytestmark = pytest.mark.django_db


def test_get_notify_team_leaders_about_tasks_overdue_soon(caplog):
    now = arrow.utcnow()
    soon_in_days = 4

    # Arrange team 1 tasks
    team_1 = baker.make(Team)
    team_1_leader = baker.make(Employee, team=team_1, is_leader=True)
    baker.make(Employee, team=team_1)
    task_to_notify_1 = baker.make(
        Task, team_assigned_to=team_1, due_time=now.shift(days=1).datetime
    )
    task_to_notify_2 = baker.make(
        Task, team_assigned_to=team_1, due_time=now.shift(days=3).datetime
    )
    baker.make(
        Task, team_assigned_to=team_1, due_time=now.shift(days=5).datetime
    )  # Noqa

    # Arrange team 2 tasks
    team_2 = baker.make(Team)
    team_2_leader = baker.make(Employee, team=team_2, is_leader=True)
    baker.make(Employee, team=team_2)
    task_to_notify_3 = baker.make(
        Task, team_assigned_to=team_2, due_time=now.shift(days=1).datetime
    )
    task_to_notify_4 = baker.make(
        Task, team_assigned_to=team_2, due_time=now.shift(days=3).datetime
    )
    baker.make(
        Task, team_assigned_to=team_2, due_time=now.shift(days=5).datetime
    )  # Noqa

    # Action
    with caplog.at_level(logging.INFO):
        caplog.clear()
        notify_team_leaders_about_tasks_overdue_soon(soon_in_days)

    # Assert
    assert len(caplog.records) == 4
    NOTIFICATION = (
        "Dummy Notification to {leader} : task {task} will be overdue soon"  # Noqa
    )
    assert caplog.records[0].__dict__["message"] == NOTIFICATION.format(
        leader=team_2_leader, task=task_to_notify_4
    )
    assert caplog.records[1].__dict__["message"] == NOTIFICATION.format(
        leader=team_2_leader, task=task_to_notify_3
    )
    assert caplog.records[2].__dict__["message"] == NOTIFICATION.format(
        leader=team_1_leader, task=task_to_notify_2
    )
    assert caplog.records[3].__dict__["message"] == NOTIFICATION.format(
        leader=team_1_leader, task=task_to_notify_1
    )
