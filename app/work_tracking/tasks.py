from datetime import datetime, timedelta

from celery.utils.log import get_task_logger
from django.utils import timezone

from core.celery.app import app
from work_tracking.models import Task
from work_tracking.services.team import get_team_leader

logger = get_task_logger(__name__)

SOON_IN_DAYS = 7


@app.task
def notify_team_leaders_about_tasks_overdue_soon():
    soon_date = (datetime.now() + timedelta(days=SOON_IN_DAYS)).date()
    today = timezone.now().date()
    tasks_overdue_tomorrow = Task.objects.select_related(
        "team_assigned_to"
    ).filter(  # Noqa
        due_time__date__gte=today, due_time__date__lte=soon_date
    )  # Noqa
    for task in tasks_overdue_tomorrow:
        task_team_leader = get_team_leader(task.team_assigned_to)
        logger.info(
            "Dummy Notification to %s : task %s will be overdue soon",
            task_team_leader,
            task,
        )
