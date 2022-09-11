from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from work_tracking.errors import LogActionNotAllowed
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
    permission_classes = [IsAuthenticated]

    def check_object_permissions(self, request, obj):
        if request.method in SAFE_METHODS:
            return True
        return self.request.user.employee == obj.employee

    def perform_create(self, serializer):
        serializer.validated_data["employee"] = self.request.user.employee
        serializer.save()

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self.check_object_permissions(self.request, self.get_object()):
            raise LogActionNotAllowed
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self.check_object_permissions(self.request, self.get_object()):
            raise LogActionNotAllowed
        return super().destroy(request, *args, **kwargs)
