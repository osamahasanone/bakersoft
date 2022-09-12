from rest_framework import serializers

from work_tracking.models import Employee, JobTitle, Team
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
                raise serializers.ValidationError("A team should have only one leader")
        return data


class TeamSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(source="employee_set", many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "created_at", "employees"]
