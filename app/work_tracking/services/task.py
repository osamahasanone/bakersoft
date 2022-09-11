from django.db import transaction

from work_tracking.models import Task
from work_tracking.serializers import TaskStateChangeSerializer


@transaction.atomic
def perform_task_transition(task: Task, serializer: TaskStateChangeSerializer):
    task.get_transition(serializer.validated_data["state"])()
    task.save()
    serializer.validated_data["task"] = task
    serializer.save()
