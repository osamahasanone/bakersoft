import pytest
from django_fsm import TransitionNotAllowed
from model_bakery import baker

from work_tracking.models import Task
from work_tracking.models.state_machine import State as TaskState
from work_tracking.serializers import TaskStateChangeSerializer
from work_tracking.services.task import perform_task_transition

pytestmark = pytest.mark.django_db


def test_perform_task_transition_success():
    task = baker.make(Task)
    state_change_data = {
        "state": TaskState.IN_PROGRESS,
        "comment": "any",
        "transitioned_at": "2022-09-20T21:40:00Z",
    }
    serializer = TaskStateChangeSerializer(data=state_change_data)
    serializer.is_valid()
    perform_task_transition(task, serializer)
    assert task.state == TaskState.IN_PROGRESS
    assert task.taskstatechange_set.count() == 1


def test_perform_task_transition_fail():
    task = baker.make(Task)
    # state cant be transitiond to COMPLETED from OPEN
    state_change_data = {
        "state": TaskState.COMPLETED,
        "comment": "any",
        "transitioned_at": "2022-09-20T21:40:00Z",
    }
    serializer = TaskStateChangeSerializer(data=state_change_data)
    serializer.is_valid()
    with pytest.raises(TransitionNotAllowed):
        perform_task_transition(task, serializer)
    assert task.state == TaskState.OPEN
    assert task.taskstatechange_set.count() == 0
