from rest_framework.viewsets import ModelViewSet

from work_tracking.models import (  # Noqa
    Employee,
    JobTitle,
    Project,
    Task,
    Team,
    WorkTimeLog,
)
from work_tracking.serializers import (
    EmployeeSerializer,
    JobTitleSerializer,
    ProjectSerializer,
    TaskSerializer,
    TeamSerializer,
    WorkTimeLogSerializer,
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


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class WorkTimeLogViewSet(ModelViewSet):
    queryset = WorkTimeLog.objects.all()
    serializer_class = WorkTimeLogSerializer
