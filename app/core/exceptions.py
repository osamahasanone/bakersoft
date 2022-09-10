from http import HTTPStatus
from typing import Any

from rest_framework.views import Response, exception_handler


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom API exception handler."""

    response = exception_handler(exc, context)

    if response is not None:
        http_code_to_message = {v.value: v.description for v in HTTPStatus}

        error_payload = {
            "error": {
                "status_code": 0,
                "message": "",
                "details": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code
        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data
        response.data = error_payload
    return response
