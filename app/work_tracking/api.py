from functools import cached_property

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from work_tracking.errors import (  # Noqa
    LogActionNotAllowed,
    TaskIsAssignedToAnotherTeam,
)
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
    ProjectStatsSerializer,
    TaskSerializer,
    TeamSerializer,
    WorkTimeLogSerializer,
)
from work_tracking.services.employee import can_add_log
from work_tracking.services.project import get_stats as get_project_stats


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

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        serializer = ProjectStatsSerializer(
            data=get_project_stats(self.get_object())
        )  # Noqa
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class WorkTimeLogViewSet(ModelViewSet):
    serializer_class = WorkTimeLogSerializer
    permission_classes = [IsAuthenticated]

    @cached_property
    def employee(self):
        return self.request.user.employee

    def get_queryset(self):
        return WorkTimeLog.objects.select_related(
            "employee", "task__project"
        ).filter(  # Noqa
            task__in=self.employee.team.task_set.all()
        )

    def check_object_permissions(self, request, obj):
        if request.method in SAFE_METHODS:
            return True
        return self.employee == obj.employee

    def perform_create(self, serializer):
        serializer.validated_data["employee"] = self.employee
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not can_add_log(self.employee, serializer.validated_data["task"]):
            raise TaskIsAssignedToAnotherTeam
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        if not self.check_object_permissions(self.request, self.get_object()):
            raise LogActionNotAllowed

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )  # Noqa
        serializer.is_valid(raise_exception=True)

        if not can_add_log(self.employee, serializer.validated_data["task"]):
            raise TaskIsAssignedToAnotherTeam

        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not self.check_object_permissions(self.request, self.get_object()):
            raise LogActionNotAllowed
        return super().destroy(request, *args, **kwargs)
