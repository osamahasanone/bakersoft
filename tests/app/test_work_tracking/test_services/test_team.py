import pytest
from model_bakery import baker

from work_tracking.models import Employee, Team
from work_tracking.services.team import get_team_leader

pytestmark = pytest.mark.django_db


def test_get_team_leader_when_existed():
    team = baker.make(Team)
    team_leader = baker.make(Employee, team=team, is_leader=True)
    baker.make(Employee, team=team)
    baker.make(Employee, team=team)
    assert get_team_leader(team) == team_leader


def test_get_team_leader_when_not_existed():
    team = baker.make(Team)
    baker.make(Employee, team=team)
    baker.make(Employee, team=team)
    assert get_team_leader(team) is None
