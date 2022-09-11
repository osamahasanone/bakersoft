from rest_framework import serializers

from work_tracking.models import (  # Noqa
    Employee,
    JobTitle,
    Project,
    Task,
    TaskStateChange,
    Team,
    WorkTimeLog,
)
from work_tracking.services.team import get_team_leader


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ["id", "name", "code", "created_at"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "user", "job_title", "team", "is_leader", "created_at"]

    def validate(self, data):
        if data["is_leader"]:
            current_team_leader = get_team_leader(data["team"])
            if current_team_leader and (
                not self.instance or self.instance != current_team_leader
            ):
                raise serializers.ValidationError(
                    "A team should have only one leader"
                )  # Noqa
        return data


class TeamSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(
        source="employee_set", many=True, read_only=True
    )  # Noqa

    class Meta:
        model = Team
        fields = ["id", "name", "created_at", "employees"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "summary",
            "description",
            "manager",
            "teams",
            "created_at",
        ]  # Noqa


class ProjectStatsSerializer(serializers.Serializer):
    estimated_hours = serializers.FloatField(allow_null=True)
    teams = serializers.IntegerField()
    active_employees = serializers.IntegerField()


class TaskStateChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStateChange
        fields = [
            "id",
            "state",
            "comment",
            "transitioned_at",
        ]  # Noqa


class TaskSerializer(serializers.ModelSerializer):
    state = serializers.CharField(read_only=True)
    state_changes = TaskStateChangeSerializer(
        source="taskstatechange_set", many=True, read_only=True
    )  # Noqa

    class Meta:
        model = Task
        fields = [
            "id",
            "summary",
            "description",
            "state",
            "project",
            "team_assigned_to",
            "start_time",
            "due_time",
            "created_at",
            "state_changes",
        ]  # Noqa

    def validate(self, data):
        if data["due_time"] <= data["start_time"]:
            raise serializers.ValidationError(
                "Due time should be after start time"
            )  # Noqa
        return data


class WorkTimeLogSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.IntegerField(
        source="task.project.id", read_only=True, default=None
    )

    class Meta:
        model = WorkTimeLog
        fields = [
            "id",
            "employee",
            "task",
            "project",
            "since",
            "until",
            "achievement",
            "details",
            "created_at",
        ]  # Noqa
