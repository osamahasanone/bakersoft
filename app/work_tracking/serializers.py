from rest_framework import serializers

from work_tracking.models import JobTitle


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ["id", "name", "code", "created_at"]
