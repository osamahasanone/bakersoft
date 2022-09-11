from rest_framework.permissions import (
    SAFE_METHODS,
    DjangoModelPermissions,
    IsAuthenticated,
)
from rest_framework.viewsets import ModelViewSet


class BaseViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, DjangoModelPermissions]
        return [permission() for permission in permission_classes]
