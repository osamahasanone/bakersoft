from functools import cached_property

from django_fsm import TransitionNotAllowed
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from work_tracking.errors import StateMachineChangeNotAllowed
from work_tracking.models import Project, Task, WorkTimeLog
from work_tracking.permissions import (
    TaskTransitionPermission,
    TimeLogAddPermission,
    TimeLogChangePermission,
)
from work_tracking.serializers import (
    ProjectSerializer,
    ProjectStatsSerializer,
    TaskSerializer,
    TaskStateChangeSerializer,
    WorkTimeLogSerializer,
)
from work_tracking.services.project import get_stats as get_project_stats
from work_tracking.services.task import perform_task_transition


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.select_related("manager").prefetch_related("teams").all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        serializer = ProjectStatsSerializer(data=get_project_stats(self.get_object()))
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related("project", "team_assigned_to").all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=["post"],
        serializer_class=TaskStateChangeSerializer,
        permission_classes=[IsAuthenticated, TaskTransitionPermission],
    )
    def transition(self, request, pk=None):
        task = self.get_object()
        serializer = TaskStateChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            perform_task_transition(task, serializer)
        except TransitionNotAllowed:
            raise StateMachineChangeNotAllowed
        return Response({})

    @action(
        detail=True,
        methods=["post"],
        serializer_class=WorkTimeLogSerializer,
        permission_classes=[IsAuthenticated, TimeLogAddPermission],
    )
    def add_log(self, request, pk=None):
        task = self.get_object()
        serializer = WorkTimeLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["employee"] = self.request.user.employee
        serializer.validated_data["task"] = task
        serializer.save()
        return Response({}, status=status.HTTP_201_CREATED)


class WorkTimeLogViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = WorkTimeLogSerializer

    @cached_property
    def employee(self):
        return self.request.user.employee

    def get_queryset(self):
        queryset = WorkTimeLog.objects.select_related("employee", "task__project").all()
        project_id = self.request.query_params.get("project_id")
        if project_id:
            return queryset.filter(
                task__project__id=project_id, task__in=self.employee.team.task_set.all()
            )
        task_ids = [task.project.id for task in self.employee.team.task_set.all()]
        projects = Project.objects.filter(id__in=task_ids)
        return queryset.filter(task__project__in=projects)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), TimeLogChangePermission()]
