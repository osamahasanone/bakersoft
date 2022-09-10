from rest_framework.viewsets import ModelViewSet

from work_tracking.models import JobTitle, Team
from work_tracking.serializers import JobTitleSerializer, TeamSerializer


class JobTitleViewSet(ModelViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
