from typing import Any, Optional

from work_tracking.models import Project, Task, WorkTimeLog


def get_estimated_hours(project: Project) -> Optional[float]:
    try:
        earliest_task = project.task_set.earliest("start_time")
        latest_task = project.task_set.latest("due_time")
        delta = latest_task.due_time - earliest_task.start_time
        return round(delta.total_seconds() / 3600, 2)
    except Task.DoesNotExist:
        return None


def get_assigned_to_teams(project: Project) -> int:
    return project.task_set.order_by().values("team_assigned_to").distinct().count()


def get_active_employees(project: Project) -> int:
    tasks = project.task_set.all()
    return (
        WorkTimeLog.objects.filter(task__in=tasks)
        .order_by()
        .values("employee")
        .distinct()
        .count()
    )


def get_stats(project: Project) -> dict[str, Any]:
    return {
        "estimated_hours": get_estimated_hours(project),
        "teams": get_assigned_to_teams(project),
        "active_employees": get_active_employees(project),
    }
