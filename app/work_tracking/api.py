from rest_framework.viewsets import ModelViewSet

from work_tracking.models import Employee, JobTitle, Project, Team
from work_tracking.serializers import (
    EmployeeSerializer,
    JobTitleSerializer,
    ProjectSerializer,
    TeamSerializer,
)


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class JobTitleViewSet(ModelViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
