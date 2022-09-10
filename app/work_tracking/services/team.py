from typing import Optional

from work_tracking.models import Employee, Team


def get_team_leader(team: Team) -> Optional[Employee]:
    return team.employee_set.filter(is_leader=True).first()
