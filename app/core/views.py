from django.http import HttpRequest
from django.template.response import SimpleTemplateResponse
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated


@api_view(http_method_names=["GET"])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def read_docs(request: HttpRequest) -> SimpleTemplateResponse:
    return SimpleTemplateResponse("swagger.html", {"schema_url": "openapi-schema"})
