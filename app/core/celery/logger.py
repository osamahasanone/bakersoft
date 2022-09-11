import logging
from typing import Dict

from celery._state import get_current_task
from celery.app.log import TaskFormatter


class TaskJSONStructuredFormatter(TaskFormatter):
    def process_log_record(self, record: logging.LogRecord) -> Dict:
        message_dict = super().process_log_record(record)

        task = get_current_task()
        if task and task.request:
            message_dict.update(task_id=task.request.id, task_name=task.name)
        else:
            message_dict.setdefault("task_name", "NA")
            message_dict.setdefault("task_id", "NA")
        return message_dict
