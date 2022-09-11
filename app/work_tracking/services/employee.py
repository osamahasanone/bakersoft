from work_tracking.models import Employee, Task


def can_add_log(employee: Employee, task: Task) -> bool:
    return not task or employee.team == task.team_assigned_to
