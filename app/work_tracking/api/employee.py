from work_tracking.api.base import BaseViewSet
from work_tracking.models import Employee, JobTitle, Team
from work_tracking.serializers import (
    EmployeeSerializer,
    JobTitleSerializer,
    TeamSerializer,
)


class TeamViewSet(BaseViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class JobTitleViewSet(BaseViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.select_related("job_title", "team").all()
    serializer_class = EmployeeSerializer
