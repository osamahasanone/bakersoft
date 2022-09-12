from rest_framework import serializers

from work_tracking.models import Project, Task, TaskStateChange, WorkTimeLog


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
        ]


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
        ]


class TaskSerializer(serializers.ModelSerializer):
    state = serializers.CharField(read_only=True)
    state_changes = TaskStateChangeSerializer(
        source="taskstatechange_set", many=True, read_only=True
    )

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
        ]

    def validate(self, data):
        if data["due_time"] <= data["start_time"]:
            raise serializers.ValidationError("Due time should be after start time")
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
        ]
