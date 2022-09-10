from rest_framework.viewsets import ModelViewSet

from work_tracking.models import JobTitle
from work_tracking.serializers import JobTitleSerializer


class JobTitleViewSet(ModelViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
